#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Text snippet extractor."""
from typing import List, Optional

from snippet import exceptions
from snippet.config import Config


class Example:
    """An example."""

    def __init__(self, path: str, line_num: int, example_name: str, line: str) -> None:
        """Initialiser."""
        self._key = (path, line_num, example_name)
        self._strip = len(line) - len(line.lstrip())
        self._text: List[str] = list()
        self._cloaking = False

    def add_line(self, line: str) -> None:
        """Adds a line."""
        if self._cloaking:
            return
        self._text.append(line)

    def cloak(self, line_num: int) -> None:
        """Starts cloaking."""
        if self._cloaking:
            raise exceptions.CloakMismatch(f"Already cloaked at {self.debug_id} ({line_num})")
        self._cloaking = True

    def uncloak(self, line_num: int) -> None:
        """Stops cloaking."""
        if not self._cloaking:
            raise exceptions.CloakMismatch(f"Already uncloaked at {self.debug_id} ({line_num})")
        self._cloaking = False

    @property
    def is_cloaking(self) -> bool:
        """States whether it's in cloaking mode."""
        return self._cloaking

    @property
    def is_empty(self) -> bool:
        """States whether the example is empty or not."""
        return len(self._text) == 0

    @property
    def text(self) -> List[str]:
        """Gets example text."""
        return self._text

    @property
    def strip_number(self) -> int:
        """Gets the example strip number."""
        return self._strip

    @property
    def key(self) -> tuple:
        """Gets the example key."""
        return self._key

    @property
    def debug_id(self) -> str:
        """Gets some debug information about the example."""
        return str(self.key)


class Examples:
    """All the examples in a file."""

    def __init__(self) -> None:
        """Initialiser."""
        self._examples: List[Example] = list()
        self._current_example: Optional[Example] = None

    def set_current(self, example: Example, line_num: int) -> None:
        """Sets current example."""
        if self._current_example:
            raise exceptions.StartEndMismatch(f"Already capturing at {self._current_example.debug_id} ({line_num})")
        self._current_example = example

    def store_current(self, line_num: int) -> None:
        """Stores current example."""
        if not self._current_example:
            raise exceptions.StartEndMismatch(f"Not yet capturing at {line_num}")
        if self._current_example.is_cloaking:
            raise exceptions.CloakMismatch(
                f"End of example reached whilst still cloaked {self._current_example.debug_id} ({line_num})"
            )
        if not self._current_example.is_empty:
            self._examples.append(self._current_example)
        self._current_example = None

    def cloak(self, line_num: int) -> None:
        """Start cloaking."""
        if self._current_example:
            self._current_example.cloak(line_num)

    def uncloak(self, line_num: int) -> None:
        """Stops cloaking."""
        if self._current_example:
            self._current_example.uncloak(line_num)

    def end(self, line_num: int) -> None:
        """Ends."""
        if self._current_example:
            raise exceptions.StartEndMismatch(
                f"EOF reached whilst still capturing {self._current_example.debug_id} ({line_num})"
            )

    def add_line(self, line: str) -> None:
        """Adds a line."""
        if self._current_example:
            self._current_example.add_line(line)

    def validate_dedent(self, line: str, line_num: int) -> None:
        """Validates dedent."""
        if not self._current_example:
            return
        if any(line[: self._current_example.strip_number].lstrip()):
            raise exceptions.ValidationFailure(
                f"Unexpected dedent whilst capturing {self._current_example.debug_id} ({line_num})"
            )

    def validate_line(self, fail_on_contains: List[str], line: str, line_num: int) -> None:
        """Validates line."""
        for trigger in fail_on_contains:
            if trigger in line:
                debug_info = self._current_example.debug_id if self._current_example else ""
                raise exceptions.ValidationFailure(f"Unexpected phrase {repr(trigger)} at {debug_info} ({line_num})")

    def clean_line(self, line: str) -> Optional[str]:
        """Cleans a line."""
        if not line:
            return None
        if not self._current_example:
            return line
        start = self._current_example.strip_number
        return line[start:].rstrip()

    @property
    def all(self) -> list:
        """Gets all the examples."""
        return self._examples


def extract_snippets_from_text(config: Config, lines: list, path: str) -> dict:
    """Finds snippets in lines of text."""
    examples = Examples()
    line_index = 0
    for line_num, line in enumerate(lines):
        line_index = line_num
        if config.start_flag in line:
            # start capturing code from the next line
            examples.set_current(
                Example(path=path, line_num=line_num, example_name=line.rsplit(":")[-1].strip(), line=line), line_num
            )
            continue

        if config.end_flag in line:
            # stop capturing, and discard empty blocks
            examples.store_current(line_num)
            continue

        if config.uncloak_flag in line:
            examples.uncloak(line_num)
            continue

        if config.cloak_flag in line:
            examples.cloak(line_num)
            continue

        # whilst capturing, append code lines to the current block
        if config.fail_on_dedent:
            examples.validate_dedent(line, line_num)
        clean_line = examples.clean_line(line)
        if not clean_line:
            continue
        if any(match in clean_line for match in config.drop_lines):
            continue
        for r_before, r_after in config.replacements.items():
            clean_line = clean_line.replace(r_before, r_after)
        examples.validate_line(config.fail_on_contains, clean_line, line_num)

        # add this line of code to the example block
        examples.add_line(clean_line)

    examples.end(line_index)
    return {example.key: example.text for example in examples.all}
