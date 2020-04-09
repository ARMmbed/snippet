#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""CLI definition."""
import argparse

import os
import sys
import dotenv

from mbed_tools_lib.logging import set_log_level, MbedToolsHandler

from snippet import config
from snippet.api import extract_code_snippets
from snippet._internal.logs import LOGGER


def main() -> int:
    """Script CLI."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, action="append", help="paths (or globs) to config files")
    parser.add_argument(
        "dir",
        nargs="?",
        default=os.getcwd(),
        help="path to project root, used by any relative paths in loaded configs [cwd]",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Set the verbosity level, enter multiple times to increase verbosity.",
    )
    parser.add_argument(
        "-t", "--traceback", action="store_true", default=True, help="Show a traceback when an error is raised."
    )
    args = parser.parse_args()
    set_log_level(args.verbose)
    dotenv.load_dotenv(dotenv.find_dotenv(usecwd=True, raise_error_if_not_found=False))
    # Use the context manager to ensure tools exceptions (expected behaviour) are shown as messages to the user,
    # but all other exceptions (unexpected behaviour) are shown as errors.
    with MbedToolsHandler(LOGGER, args.traceback):
        extract_code_snippets(config.get_config(config_paths=args.config, project_root=args.dir,))
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
