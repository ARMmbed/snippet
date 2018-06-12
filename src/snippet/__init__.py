import logging
import textwrap

from snippet.config import Config
from snippet.workflow import run


def main(config: Config):
    if config.log_level:
        logging.basicConfig(level=config.log_level)
    logger = logging.getLogger(__name__)
    logger.debug('project directory is %r', config.project_root)
    examples, paths, failures = run(config)

    if failures:
        logger.error('failures:\n%s', textwrap.indent('\n'.join(f'{name}: {exc}' for name, exc in failures), prefix='  '))
        raise Exception(f'There were %s failures!' % len(failures))
