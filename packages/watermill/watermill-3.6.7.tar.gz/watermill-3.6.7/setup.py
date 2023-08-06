from os import path

from setuptools import find_packages
from setuptools import setup

readme_file_path = path.join(path.abspath(path.dirname(__file__)), 'README.md')
with open(readme_file_path, encoding='utf-8') as readme_file:
    long_description = readme_file.read()

setup(
    name='watermill',
    version='3.6.7',
    url='https://gitlab.com/kraevs/watermill',
    project_urls={
        'Code': 'https://gitlab.com/kraevs/watermill',
        'Issue tracker': 'https://gitlab.com/kraevs/watermill/issues'
    },
    description='Watermill data stream organizing framework.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Stanislav Kraev',
    author_email='stanislav.kraev@gmail.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    packages=find_packages(),
    platforms='any',
    python_requires='>=3.6',
    install_requires=[
        'botox-di==1.5.0',
        'dataclasses;python_version<"3.7"',
        'dataclass-factory==2.8.1'
    ]
)
