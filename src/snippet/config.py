import glob
import logging
import os

import toml


class Config:
    # IO
    project_root = '.'  # the project root used for relative IO paths (set by commandline)
    input_glob = 'tests/example/*.py'
    output_template = '```python\n# example: {{{name}}}\n{{{code}}}\n```\n'  # a mustache template for each file
    output_append = False  # if the output file exists, append to it
    output_dir = '.'
    output_file_ext = 'md'

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


def find_config(root):
    return (
        glob.glob(os.path.join(root, '**', '*.toml'), recursive=True) +
        glob.glob(os.path.join(root, '**', '*.cfg'), recursive=True)
    )


def get_config(config_path=None, **options):
    config = Config()
    project_root = os.path.abspath(options.get('project_root', config.project_root))

    new_options = {}
    config_path = config_path or os.environ.get('SNIPPET_CONFIG_PATH')
    toml_files = [config_path] if config_path else find_config(root=project_root)
    for toml_file in toml_files:
        logging.debug('trying config from %s', toml_file)
        with open(toml_file) as f:
            try:
                config_file_contents = toml.load(f)
            except toml.TomlDecodeError as e:
                logging.debug('failed to load %s: %s', toml_file, e)
                continue
            snippet_config = config_file_contents.get('snippet')
            if snippet_config:
                logging.info('loading config from %s', toml_file)
                new_options.update(snippet_config)

    # passed keyword args override other parameters
    new_options.update(options)

    # update the config object
    for k, v in new_options.items():
        setattr(config, k, v)

    # validate and set IO directories that are relative to project root
    config.input_glob = os.path.abspath(os.path.join(config.project_root, config.input_glob))
    config.output_dir = os.path.abspath(os.path.join(config.project_root, config.output_dir))
    return config
