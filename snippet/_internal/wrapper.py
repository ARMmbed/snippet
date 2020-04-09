#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Decorator."""
import traceback
from snippet.config import Config
from typing import Callable, Any, List


def wrap(config: Config, failures: List[Any], identifier: str, nullary_function: Callable, default: Any = None) -> Any:
    """Executes a function (`nullary_function`) with no arguments.

    to pass arguments, use partials
    stores any exceptions in `failures`
    """
    try:
        return nullary_function()
    except Exception:
        if config.stop_on_first_failure:
            raise
        failures.append((identifier, traceback.format_exc()))
    return default
