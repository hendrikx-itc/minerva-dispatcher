"""Tests that start the dispatcher as a sub-process."""
import os
from subprocess import Popen, PIPE
import json
from time import sleep
from datetime import datetime
from contextlib import closing

from nose.tools import eq_

from minerva.instance import MinervaInstance
from minerva.system.jobsource import JobSource


TEST_CONFIG = """\
log_directory = /tmp/
log_filename = dispatcher.log
log_rotation_size = 10MB
log_level = INFO

[database]
user=dispatcher
"""


def test_cmd_1():
    config_file_path = "/tmp/dispatcher_test/dispatcher.conf"
    data_dir = '/tmp/dispatcher_test/data'
    db_user = 'minerva_admin'

    with open(config_file_path, "w") as config_file:
        config_file.write(TEST_CONFIG)

    try:
        os.stat(data_dir)
    except OSError:
        os.makedirs(data_dir)

    minerva_instance = MinervaInstance.load('default')

    jobsource_config = {
        'uri': data_dir,
        'recursive': False,
        'match_pattern': r'.*\.csv',
        'job_config': {
            'datatype': 'dummy',
            'datasource': 'integration-test',
            'parser_config': {}
        }
    }

    jobsource = JobSource(
        id=None, name='integration-test', job_type='harvest',
        config=json.dumps(jobsource_config))

    with closing(minerva_instance.connect(user=db_user)) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute('DELETE FROM system.job_source')
            jobsource.create(cursor)

        conn.commit()

    cmd = ["dispatcher", "-c", config_file_path]
    p = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE)

    sleep(2)

    timestamp = datetime.now()
    file_name = "test_{}.csv".format(timestamp)
    file_path = os.path.join(data_dir, file_name)
    create_dummy_file(file_path)

    sleep(2)

    p.terminate()

    with closing(minerva_instance.connect(user=db_user)) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute("SELECT * FROM system.job")

            job_rows = cursor.fetchall()

    eq_(len(job_rows), 1)


def create_dummy_file(file_path):
    with open(file_path, "w") as test_file:
        test_file.write(
            "type, name, a, b, c\n"
            "Node, 001, 12, 232, high\n"
            "Node, 002, 43, 334, medium\n")
