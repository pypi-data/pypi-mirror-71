"""
This file is part of the tagup Python module which is released under MIT.
See file LICENSE for full license details.
"""


# Base.

class TagupError(Exception):
    def __init__(self, message, tag_stack_trace=None):
        super().__init__(message)
        self.tag_stack_trace = tag_stack_trace


# Standalone.

class ImproperlyConfigured(TagupError):
    pass


class TagupSyntaxError(TagupError):
    pass


# Rendering

class TagupRenderingError(TagupError):
    pass


class TagNotFound(TagupRenderingError):
    pass


class ArgumentMissing(TagupRenderingError):
    pass


class NamedArgumentMissing(ArgumentMissing):
    pass


class PositionalArgumentMissing(ArgumentMissing):
    pass


# Stack.

class TagStackError(TagupError):
    pass


class TagStackUnderflow(TagStackError):
    pass


class TagStackOverflow(TagStackError):
    pass
