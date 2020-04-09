#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Snippet exceptions."""


class SnippetError(Exception):
    """Generic error."""

    pass


class DuplicateName(SnippetError):
    """Found duplicated names."""

    pass


class ValidationFailure(SnippetError):
    """Failed snippet validation."""

    pass


class TagMismatch(SnippetError):
    """Tags mismatch in snippet."""

    pass


class StartEndMismatch(TagMismatch):
    """Snippet format problem."""

    pass


class CloakMismatch(TagMismatch):
    """Invalid cloaking in snippet."""

    pass
