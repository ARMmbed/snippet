#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Code Snippet APIs."""
import textwrap

from snippet import workflow, config
from snippet._internal.logs import LOGGER


def extract_code_snippets(config: config.Config) -> None:
    """Extracts code snippets according to configuration."""
    LOGGER.debug("project directory is %r", config.project_root)
    examples, paths, failures = workflow.run(config)

    if failures:
        LOGGER.error(
            "failures:\n%s", textwrap.indent("\n".join(f"{name}: {exc}" for name, exc in failures), prefix="  ")
        )
        raise Exception(f"There were %s failures!" % len(failures))
