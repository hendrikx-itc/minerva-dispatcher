# -*- coding: utf-8 -*-

from setuptools import setup

setup(name="dispatcher",
    version="4.4.0",
    install_requires=["configobj",
        "minerva>=3.0.0", "pyinotify"],
    test_suite="nose.collector",
    package_data={"minerva_dispatcher": ["defaults/*"]},
    packages=["minerva_dispatcher"],
    package_dir={"": "src"},
    scripts=["scripts/dispatcher", "scripts/enqueue-job", "scripts/sweep-jobs"])
