#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Definition of the full workflow."""
import textwrap
from functools import partial
from pathlib import Path
from typing import Tuple, Any, List, Dict

from snippet import exceptions
from snippet._internal import file_wrangler
from snippet._internal.logs import LOGGER
from snippet._internal.util import ensure_list
from snippet._internal.wrapper import wrap
from snippet.config import Config
from snippet.snippet import extract_snippets_from_text


def run(config: Config) -> Tuple[dict, list, list]:
    """Retrieves all the code snippets according to configuration."""
    failures: List[Any] = list()

    _set_config(config)
    examples, paths = _find_all_code_examples(config, failures)

    _check_for_duplicates(examples)

    for (path, line_num, example_name), code_lines in examples.items():
        example_block = "\n".join(code_lines)
        LOGGER.info("example: %r", example_name)
        LOGGER.debug("example code: %s", example_block)

        wrap(config, failures, path, partial(file_wrangler.write_example, config, example_name, example_block))

    return examples, paths, failures


def _check_for_duplicates(examples: dict) -> None:
    unique_example_names: Dict[str, Any] = dict()
    for (path, line_num, example_name), code_lines in examples.items():
        existing = unique_example_names.get(example_name)
        if existing:
            raise exceptions.DuplicateName("Example with duplicate name %s %s matches %s" % (path, line_num, existing))
        else:
            unique_example_names[example_name] = (path, line_num, example_name)


def _set_config(config: Config) -> None:
    # validate and set IO directories that are relative to project root
    config.input_glob = [
        str(Path(config.project_root).joinpath(str(pattern)).absolute()) for pattern in ensure_list(config.input_glob)
    ]
    config.output_dir = str(Path(config.project_root).joinpath(config.output_dir).absolute())


def _find_all_code_examples(config: Config, failures: List[Any]) -> Tuple[dict, list]:
    paths = file_wrangler.find_files(config)
    LOGGER.debug("files to parse:\n%s", textwrap.indent("\n".join(paths), prefix="  "))
    examples = dict()

    for path in paths:
        # load the file
        lines = wrap(config, failures, path, partial(file_wrangler.load_file_lines, path), [])

        # extract snippets
        new_examples = wrap(config, failures, path, partial(extract_snippets_from_text, config, lines, path), {})

        # store the new examples for analysis
        examples.update(new_examples)
    return examples, paths
