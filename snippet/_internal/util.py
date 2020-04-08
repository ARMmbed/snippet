#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Utilities."""
from typing import Any


def ensure_list(item: Any) -> list:
    """Ensures an item is a list."""
    if item:
        return item if isinstance(item, list) else [item]
    return list()
