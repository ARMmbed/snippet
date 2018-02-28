import logging

from snippet.config import Config
from snippet.workflow import run


def main(config: Config):
    if config.log_level:
        logging.basicConfig(level=config.log_level)

    examples, failures = run(config)

    if failures:
        raise Exception(f'There were failures!:\n{failures}')
