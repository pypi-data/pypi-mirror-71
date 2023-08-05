import json
from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from logging import getLogger
from time import time
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Mapping
from typing import Optional
from typing import Type

from kafka import KafkaConsumer
from kafka import KafkaProducer
from kafka import OffsetAndMetadata
from kafka import TopicPartition

from watermill.message_brokers.message_broker import DataKey
from watermill.message_brokers.message_broker import EndOfStream
from watermill.message_brokers.message_broker import EndOfStreamError
from watermill.message_brokers.message_broker import MessageBroker
from watermill.message_brokers.message_broker import RightJoinedStreamRanAhead
from watermill.message_brokers.message_broker import StreamTimeoutError
from watermill.message_brokers.message_broker import StreamType
from watermill.message_brokers.message_broker import StreamsShift


logger = getLogger(__name__)


@dataclass
class ConsumerTopicOffset:
    consumer: KafkaConsumer
    topic_name: str
    offset: int


@dataclass
class KafkaDataKey(DataKey):
    consumer_offsets: List[ConsumerTopicOffset] = field(default_factory=list)


class KafkaMessageBroker(MessageBroker):
    def __init__(
            self,
            topic_names: Mapping[Type[StreamType], str],
            kafka_url: str,
            data_timeout: Optional[int] = None,
            poll_timeout: Optional[int] = None,
            consumer_group_name: Optional[str] = None,
            kafka_extra_args: Optional[dict] = None
    ):
        assert topic_names

        self._kafka_url = kafka_url
        self._serializers = {}
        self._topic_names = topic_names
        self._consumers = {}
        self._kafka_extra_args = kafka_extra_args or {}
        self._producer = self._initialize_producer()
        self._data_timeout_ms = data_timeout or 60 * 60 * 1000
        self._poll_timeout_ms = poll_timeout
        if not self._poll_timeout_ms:
            self._poll_timeout_ms = self._data_timeout_ms
        self._consumer_group_name = consumer_group_name or 'watermill'
        self._partitions = {}
        self._stepped_back_element = {}

    def get_elements(
            self,
            element_type: Type[StreamType],
            comparator: Callable[[Any, Any], StreamsShift] = None
    ) -> dict:
        if element_type not in self._consumers:
            group_id = element_type.__name__
            if self._consumer_group_name:
                group_id = self._consumer_group_name + '-' + group_id
            self._consumers[element_type] = self._initialize_consumer(
                topic_name=self._topic_names[element_type],
                group_id=group_id,
                stream_type=element_type,
            )

        consumer = self._consumers[element_type]

        if comparator and self._stepped_back_element.get(element_type):
            if comparator(self._stepped_back_element.get(element_type)) == StreamsShift.Less:
                return

        element = self._get_next_element(element_type, consumer)
        self._stepped_back_element.pop(element_type, None)
        if not comparator:
            yield element
            return

        while comparator(element) == StreamsShift.Greater:
            logger.warning(f'Skipped stream {element_type} element')
            element = self._get_next_element(element_type, consumer)

        if comparator(element) == StreamsShift.Less:
            self._step_back(element_type)
            self._stepped_back_element[element_type] = element
            raise RightJoinedStreamRanAhead(element_type)

        while comparator(element) == StreamsShift.Equal:
            yield element
            try:
                element = self._get_next_element(element_type, consumer)
            except EndOfStreamError:
                self._step_back(element_type)
                self._stepped_back_element[element_type] = element
                raise

        self._step_back(element_type)
        self._stepped_back_element[element_type] = element

    def commit(self, data_key: Optional[DataKey] = None):
        assert self._consumers
        assert data_key is None or isinstance(data_key, KafkaDataKey)
        if not data_key:
            for stream_type in self._topic_names.keys():
                if stream_type in self._consumers:
                    consumer = self._consumers[stream_type]
                    logger.debug(f'committing {stream_type} stream')
                    consumer.commit()
                    partition = self._partitions[stream_type]
                    logger.debug(f'{stream_type} stream committed offset: {consumer.position(partition)}')
        else:
            for consumer_topic_offset in data_key.consumer_offsets:
                consumer = consumer_topic_offset.consumer
                offsets: Dict[TopicPartition, OffsetAndMetadata] = {
                    TopicPartition(consumer_topic_offset.topic_name, 0): OffsetAndMetadata(consumer_topic_offset.offset, '')
                }
                consumer.commit(offsets)

    def send(self, item_type: Type[StreamType], item: dict):
        self._producer.send(self._topic_names[item_type], json.dumps(item, ensure_ascii=False).encode('utf8'))
        self._producer.flush()

    def send_eos(self, item_type: Type[StreamType]):
        self._producer.send(self._topic_names[item_type], json.dumps(asdict(EndOfStream()), ensure_ascii=False).encode('utf8'))
        self._producer.flush()

    def get_data_key(self) -> Optional[DataKey]:
        consumer_offsets = []
        for element_type, consumer in self._consumers.items():
            partition = self._partitions[element_type]
            consumer_offsets.append(ConsumerTopicOffset(
                consumer=consumer,
                topic_name=self._topic_names[element_type],
                offset=consumer.position(partition)
            ))
        return KafkaDataKey(consumer_offsets=consumer_offsets)

    def _initialize_consumer(self, topic_name: str, group_id: str, stream_type: Type[StreamType]) -> KafkaConsumer:
        consumer = KafkaConsumer(
            bootstrap_servers=self._kafka_url,
            group_id=group_id,
            auto_offset_reset='earliest',
            enable_auto_commit=False,
            max_poll_records=1,
            **self._kafka_extra_args,
        )
        partition = TopicPartition(topic_name, 0)
        self._partitions[stream_type] = partition
        consumer.assign([partition])
        logger.debug(f'{topic_name} topic startup offset: {consumer.position(partition)}')
        return consumer

    def _initialize_producer(self) -> KafkaProducer:
        return KafkaProducer(bootstrap_servers=self._kafka_url, **self._kafka_extra_args)

    def _get_next_element(self, element_type: Type[StreamType], consumer: KafkaConsumer) -> dict:
        timeout = self._poll_timeout_ms
        params = {'timeout_ms': timeout} if timeout else {}
        with _TimerContext() as timer:
            next_elements = consumer.poll(**params)
        if not next_elements:
            if timer.elapsed >= self._data_timeout_ms or self._poll_timeout_ms is None:
                raise EndOfStreamError(stream_type=element_type)

            raise StreamTimeoutError(stream_type=element_type)

        for topic, list_of_records in next_elements.items():
            assert len(list_of_records) == 1
            record = list_of_records[0]
            data_bytes = record.value
            element = json.loads(data_bytes.decode('utf8'))

        if element.get('eos__'):
            raise EndOfStreamError(stream_type=element_type)
        return element

    def _step_back(self, element_type: Type[StreamType]):
        consumer = self._consumers[element_type]
        partition = self._partitions[element_type]
        offset = consumer.position(partition)
        consumer.seek(partition, offset - 1)
        logger.debug(f'seek backward 1 message for {element_type}')


class _TimerContext:
    def __init__(self):
        self._start_time = 0
        self._end_time = 0

    def __enter__(self):
        self._start_time = self._end_time = time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._end_time = time()

    @property
    def elapsed(self):
        return self._end_time - self._start_time
