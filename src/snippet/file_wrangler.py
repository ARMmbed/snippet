import logging
import os
import glob

import pystache

from snippet.config import Config


def write_example(config: Config, path, example_name, example_block):
    """Writes example to file"""
    output = pystache.render(
        config.output_template,
        name=example_name,
        code=example_block
    )
    if not os.path.exists(config.output_dir):
        os.makedirs(config.output_dir)
    # TODO: this, properly...
    clean_name = example_name.strip().replace(' ', '')
    output_file = os.path.join(config.output_dir, clean_name) + os.extsep + config.output_file_ext
    logging.info('writing %r to %s', example_name, output_file)
    with open(output_file, 'a' if config.output_append else 'w') as fh:
        fh.write(output)


def load_file_lines(path):
    """Loads file into memory"""
    with open(path, 'r', encoding='utf8') as fh:
        lines = fh.readlines()
    return lines


def find_files(config: Config):
    """Finds input file paths, according to the config"""
    return glob.glob(config.input_glob)
