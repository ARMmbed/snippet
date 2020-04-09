#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Definition of the configuration of snippet."""
import glob
import logging
import os
from pathlib import Path

import toml

from snippet._internal.logs import LOGGER
from snippet._internal.util import ensure_list
from typing import Optional, List


class EnvironmentVariables:
    """Environment variables used by snippet."""

    @property
    def SNIPPET_CONFIG_PATH(self) -> Optional[str]:
        """Path to the configuration file for snippet."""
        return os.getenv("SNIPPET_CONFIG_PATH")


DEFAULT_PROJECT_ROOT_PATH = "."


class Config:
    """Definition of snippet's configuration."""

    # IO
    project_root = DEFAULT_PROJECT_ROOT_PATH  # the project root used for relative IO paths (set by commandline)
    input_glob = ["tests/example/*.py"]
    output_append = True  # if the output file exists, append to it
    output_dir = "."
    output_file_name_template = "{{name}}.md"  # a mustache template for the output file name
    write_attempts = 3  # number of retries when writing output files

    # Language and style
    language_name = "python"
    comment_prefix = "# "
    comment_suffix = ""
    # a mustache template for each file (triple braces important for code literals, no escaping)
    output_template = "```{{language_name}}\n{{comment_prefix}}example: {{{name}}}{{comment_suffix}}\n{{{code}}}\n```\n"

    # Logger
    log_level = logging.INFO

    # Code block indicators
    start_flag = "an example"
    end_flag = "end of example"

    # Hidden block indicators
    cloak_flag = "cloak"
    uncloak_flag = "uncloak"

    # Validation and formatting logic
    drop_lines: List[str] = list()  # drop lines containing these phrases
    replacements = {"self.": ""}  # straightforward replacements
    fail_on_contains = ["assert"]  # fail if these strings are found in code blocks
    auto_dedent = True  # keep code left-aligned with the start flag
    fail_on_dedent = True  # fail if code is dedented before reaching the end flag
    stop_on_first_failure = False  # fail early


def get_config(config_paths: Optional[list] = None, **options: dict) -> Config:
    """Gets Snippet's configuration."""
    config = Config()
    config_paths = _determine_config_paths(config_paths, options)
    new_options = _load_configs(config_paths)

    # passed keyword args override other parameters
    new_options.update(options)

    # update the config object
    for k, v in new_options.items():
        setattr(config, k, v)

    return config


def _load_configs(config_paths: list) -> dict:
    """Loads all the config files."""
    new_options = {}
    for toml_file in _find_configs(glob_patterns=config_paths):
        LOGGER.debug("trying config from %s", toml_file)
        with open(toml_file, encoding="utf8") as f:
            try:
                config_file_contents = toml.load(f)
            except toml.TomlDecodeError as e:
                LOGGER.debug("failed to load %s: %s", toml_file, e)
                continue
            snippet_config = config_file_contents.get("snippet")
            if snippet_config:
                LOGGER.info("loading config from %s", toml_file)
                new_options.update(snippet_config)
    return new_options


def _find_configs(glob_patterns: list) -> list:
    """Finds all the different configuration files on the file system."""
    configs = []
    for glob_pattern in glob_patterns:
        configs.extend(glob.glob(glob_pattern, recursive=True))
    return configs


def _config_paths_from_env() -> list:
    """Gets configuration paths from environment."""
    return ensure_list(EnvironmentVariables().SNIPPET_CONFIG_PATH)


def _determine_config_paths(config_paths: Optional[list], options: dict) -> list:
    """Determines the paths to all configuration files."""
    project_root = Path(options.get("project_root", DEFAULT_PROJECT_ROOT_PATH)).absolute()

    config_paths = config_paths or list()
    config_paths.extend(_config_paths_from_env())
    # fallback option - search the project directory
    if len(config_paths) == 0:
        config_paths.append(str((project_root.joinpath("**", "*.toml"))))
    return config_paths
