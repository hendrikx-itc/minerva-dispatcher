# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name="dispatcher",
    author='Hendrikx ITC',
    author_email='info@hendrikx-itc.nl',
    version="5.0,0.dev2",
    license='GPL',
    description='Minerva Dispatcher library and commands',
    python_requires='>=3.5',
    install_requires=[
        "configobj",
        "minerva-etl>=5.0.0",
        "pyinotify",
        "pyyaml",
        "pika"
    ],
    test_suite="nose.collector",
    package_data={"minerva_dispatcher": ["defaults/*"]},
    packages=["minerva_dispatcher"],
    package_dir={"": "src"},
    scripts=["scripts/dispatcher"]
)
