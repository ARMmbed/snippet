class SnippetError(Exception):
    pass


class DuplicateName(SnippetError):
    pass


class ValidationFailure(SnippetError):
    pass


class TagMismatch(SnippetError):
    pass


class StartEndMismatch(TagMismatch):
    pass


class CloakMismatch(TagMismatch):
    pass
