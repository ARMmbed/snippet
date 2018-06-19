import textwrap
import os
from functools import partial

from snippet import file_wrangler
from snippet.config import Config
from snippet.snippet import extract_snippets
from snippet.wrapper import wrap
from snippet import exceptions
from snippet.logs import logger
from snippet.util import ensure_list


def run(config: Config):
    examples = {}
    failures = []

    # validate and set IO directories that are relative to project root
    config.input_glob = [
        os.path.abspath(os.path.join(config.project_root, pattern)) for pattern in ensure_list(config.input_glob)
    ]
    config.output_dir = os.path.abspath(os.path.join(config.project_root, config.output_dir))

    paths = file_wrangler.find_files(config)
    logger.debug('files to parse:\n%s', textwrap.indent('\n'.join(paths), prefix='  '))

    for path in paths:
        # load the file
        lines = wrap(config, failures, path, partial(
            file_wrangler.load_file_lines, path
        ), [])

        # extract snippets
        new_examples = wrap(config, failures, path, partial(
            extract_snippets, config, lines, path
        ), {})

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
        logger.info('example: %r', example_name)
        logger.debug('example code: %s', example_block)

        wrap(config, failures, path, partial(
            file_wrangler.write_example, config, example_name, example_block
        ))

    return examples, paths, failures
