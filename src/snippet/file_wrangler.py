import os
import glob

import pystache

from snippet.config import Config
from snippet.logs import logger


def write_example(config: Config, example_name, example_block):
    """Writes example to file"""
    output = pystache.render(
        config.output_template,
        name=example_name,
        code=example_block,
        comment_prefix=config.comment_prefix,
        comment_suffix=config.comment_suffix,
        language_name=config.language_name
    )

    output_file_name = pystache.render(
        config.output_file_name_template,
        name=example_name.strip().replace(' ', '_').lower()
    )

    if not os.path.exists(config.output_dir):
        logger.info('creating output directory %s', config.output_dir)
        os.makedirs(config.output_dir)
    output_file = os.path.join(config.output_dir, output_file_name)
    logger.info('writing %r to %s', example_name, output_file)
    with open(output_file, 'a' if config.output_append else 'w') as fh:
        fh.write(output)


def load_file_lines(path):
    """Loads file into memory"""
    with open(path, 'r', encoding='utf8') as fh:
        lines = fh.readlines()
    return lines


def find_files(config: Config):
    """Finds input file paths, according to the config"""
    files = []
    for glob_pattern in config.input_glob:
        files.extend(glob.glob(glob_pattern, recursive=True))
    return files
