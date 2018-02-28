import logging
import os

import toml


class Config:
    # IO
    input_glob = 'tests/example/*.py'
    output_template = '```python\n# example: {{name}}{{code}}\n```'  # a mustache template for each file
    output_append = False  # if the output file exists, append to it
    output_dir = None

    # Logging
    log_level = logging.INFO

    # Code block indicators
    start_flag = 'an example'
    end_flag = 'end of example'

    # Hidden block indicators
    cloak_flag = 'cloak'
    uncloak_flag = 'uncloak'

    # Validation and formatting logic
    replacements = {'self.': ''}  # straightforward replacements
    fail_on_contains = ['assert']  # fail if these strings are found in code blocks
    auto_dedent = True  # keep code left-aligned with the start flag
    fail_on_dedent = True  # fail if code is dedented before reaching the end flag
    stop_on_first_failure = False  # fail early


def get_config(config_path=None, **options):
    new_options = {}
    if config_path or os.environ.get('SNIPPET_CONFIG_PATH'):
        with open(config_path) as f:
            new_options.update(toml.load(f))
    new_options.update(options)
    config = Config()
    for k, v in new_options:
        setattr(config, k, v)
    return config
