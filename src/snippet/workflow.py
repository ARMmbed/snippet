import logging
import textwrap
from functools import partial

from snippet import file_wrangler
from snippet.config import Config
from snippet.snippet import extract_snippets
from snippet.wrapper import wrap
from snippet import exceptions


def run(config: Config):
    examples = {}
    failures = []
    paths = file_wrangler.find_files(config)
    logging.debug('files to parse:\n%s', textwrap.indent('\n'.join(paths), prefix='  '))

    for path in paths:
        # load the file
        lines = wrap(config, failures, path, partial(
            file_wrangler.load_file_lines, path
        ))

        # extract snippets
        new_examples = wrap(config, failures, path, partial(
            extract_snippets, config, lines, path
        ))

        # store the new examples for analysis
        examples.update(new_examples)

    unique_example_names = dict()
    for (path, line_num, example_name), code_lines in examples.items():
        existing = unique_example_names.get(example_name)
        if existing:
            raise exceptions.DuplicateName('Example with duplicate name %s %s matches %s' % (path, line_num, existing))
        else:
            unique_example_names[example_name] = (path, line_num, example_name)

    for (path, line_num, example_name), code_lines in examples.items():
        example_block = '\n'.join(code_lines)
        logging.info('example: %r', example_name)
        logging.debug('example code: %s', example_block)

        wrap(config, failures, path, partial(
            file_wrangler.write_example, config, path, example_name, example_block
        ))

    return examples, paths, failures
