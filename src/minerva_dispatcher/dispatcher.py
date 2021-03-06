"""
Minerva Dispatcher command line script.

Dispatcher/harvest job sources look like this:

{
    "uri": "/data",
    "recursive": true,
    "match_pattern": ".*",
    "job_config": {}
}

"""
import os
import argparse
import logging.handlers

import yaml

from minerva_dispatcher.version import __version__ as version
from minerva_dispatcher import JobCollector, get_job_sources

package_name = "minerva_dispatcher"
script_name = os.path.basename(__file__)
config_file_name = "dispatcher.yml"


def main():
    """Script entry point."""
    parser = argparse.ArgumentParser(
        description="watch job sources for new files/jobs"
    )

    parser.add_argument(
        "--version", action="version", version='%(prog)s {}'.format(version),
        help="display version information and exit"
    )

    parser.add_argument(
        "--debug", action="store_true", default=False,
        help="Enable debug logging"
    )

    parser.add_argument(
        "-c", "--config-file",
        default=os.path.join("/etc/minerva/", config_file_name),
        help="path of configuration file"
    )

    args = parser.parse_args()

    config = load_config(args.config_file)

    job_sources = get_job_sources(config)
    job_collector = JobCollector(job_sources, config['rabbitmq'])
    job_collector.start()

    root_logger = logging.getLogger()

    if args.debug:
        root_logger.setLevel(logging.DEBUG)
    else:
        root_logger.setLevel(logging.INFO)

    logging.info("started with pid {0:d}".format(os.getpid()))

    try:
        job_collector.run()
    except Exception as e:
        logging.warning("error in loop: {}".format(e))
        raise e
    else:
        logging.warning("loop ended")
    finally:
        job_collector.stop()
        logging.info("collector stopped")


def load_config(file_path):
    with open(file_path) as config_file:
        return yaml.load(config_file, Loader=yaml.SafeLoader)
