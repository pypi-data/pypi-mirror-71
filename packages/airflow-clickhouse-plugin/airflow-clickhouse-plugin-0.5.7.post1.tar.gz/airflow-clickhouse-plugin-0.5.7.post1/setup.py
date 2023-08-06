#!/usr/bin/env python3

import os
from setuptools import setup, find_packages

# get key package details from airflow_clickhouse_plugin/__version__.py
about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'airflow_clickhouse_plugin', '__version__.py')) as f:
    exec(f.read(), about)

# load the README file and use it as the long_description for PyPI
with open(os.path.join(here, 'README.md'), 'r') as f:
    readme = f.read()

setup(
    name=about['__title__'],
    description=about['__description__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    version=about['__version__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    packages=find_packages(exclude=('tests',)),
    include_package_data=True,
    python_requires=">=3.6.*",
    install_requires=[
        'clickhouse-driver~=0.1.2',
        'apache-airflow~=1.10.6',  # TODO has to be ==1.10.6 for testing to not rely on future features
    ],
    license=about['__license__'],
    zip_safe=False,
    entry_points={
        'airflow.plugins': [
            'airflow_clickhouse_hook '
                '= airflow_clickhouse_plugin:ClickHouseHookPlugin',
            'airflow_clickhouse_operator '
                '= airflow_clickhouse_plugin:ClickHouseOperatorPlugin',
            'airflow_clickhouse_sql_sensor '
                '= airflow_clickhouse_plugin:ClickHouseSqlSensorPlugin',
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.6',
    ],
    keywords=['clickhouse', 'airflow'],
)
