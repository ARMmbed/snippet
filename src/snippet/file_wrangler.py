import pystache
import glob

from snippet.config import Config


def write_example(config: Config, path, example_name, example_block):
    """Writes example to file"""
    output = pystache.render(
        config.output_template,
        name=example_name,
        code=example_block
    )
    with open(path, 'a' if config.output_append else 'w') as fh:
        fh.write(output)


def load_file_lines(path):
    """Loads file into memory"""
    with open(path, 'r') as fh:
        lines = fh.readlines()
    return lines


def find_files(config: Config):
    """Finds input file paths, according to the config"""
    return glob.glob(config.input_glob)
