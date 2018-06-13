import logging
import glob
import os

import toml

from snippet.logs import logger
from snippet.util import ensure_list


class Config:
    # IO
    project_root = '.'  # the project root used for relative IO paths (set by commandline)
    input_glob = 'tests/example/*.py'
    output_append = True  # if the output file exists, append to it
    output_dir = '.'
    output_file_name_template = '{{name}}.md'  # a mustache template for the output file name

    # Language and style
    language_name = 'python'
    comment_prefix = '# '
    comment_suffix = ''
    # a mustache template for each file (triple braces important for code literals, no escaping)
    output_template = '```{{language_name}}\n{{comment_prefix}}example: {{{name}}}{{comment_suffix}}\n{{{code}}}\n```\n'

    # logger
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


def find_configs(glob_patterns):
    configs = []
    for glob_pattern in glob_patterns:
        configs.extend(glob.glob(glob_pattern, recursive=True))
    return configs


def config_paths_from_env():
    env_var = os.environ.get('SNIPPET_CONFIG_PATH')
    return list(env_var) if env_var else []


def get_config(config_paths=None, **options):
    config = Config()
    project_root = os.path.abspath(options.get('project_root', config.project_root))

    new_options = {}

    config_paths = config_paths or []
    config_paths.extend(config_paths_from_env())

    # fallback option - search the project directory
    if not config_paths:
        config_paths.append(os.path.join(project_root, '**', '*.toml'))

    for toml_file in find_configs(glob_patterns=config_paths):
        logger.debug('trying config from %s', toml_file)
        with open(toml_file) as f:
            try:
                config_file_contents = toml.load(f)
            except toml.TomlDecodeError as e:
                logger.debug('failed to load %s: %s', toml_file, e)
                continue
            snippet_config = config_file_contents.get('snippet')
            if snippet_config:
                logger.info('loading config from %s', toml_file)
                new_options.update(snippet_config)

    # passed keyword args override other parameters
    new_options.update(options)

    # update the config object
    for k, v in new_options.items():
        setattr(config, k, v)

    # validate and set IO directories that are relative to project root
    config.input_glob = [
        os.path.abspath(os.path.join(config.project_root, pattern)) for pattern in ensure_list(config.input_glob)
    ]
    config.output_dir = os.path.abspath(os.path.join(config.project_root, config.output_dir))
    return config
