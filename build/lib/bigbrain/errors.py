"""BigBrain error types.

UserError and its subclasses represent user-facing failures that should
be displayed *without* stack traces at the CLI boundary.  Internal or
unexpected exceptions should propagate normally.
"""


class UserError(Exception):
    """Base exception for user-facing errors.

    Raise for predictable failure modes: bad CLI input, missing config,
    unsupported file formats, etc.  The CLI layer catches these and
    shows the message concisely.
    """


class IngestionError(UserError):
    """Error during file ingestion."""


class UnsupportedFormatError(IngestionError):
    """Raised when a file type is not supported for ingestion."""

    def __init__(self, extension: str, path: str = ""):
        self.extension = extension
        self.path = path
        msg = f"Unsupported file format: '{extension}'"
        if path:
            msg += f" ({path})"
        super().__init__(msg)


class FileAccessError(IngestionError):
    """Raised when a file cannot be read or accessed."""

    def __init__(self, path: str, reason: str = ""):
        self.path = path
        self.reason = reason
        msg = f"Cannot access file: {path}"
        if reason:
            msg += f" ({reason})"
        super().__init__(msg)


class ConfigError(UserError):
    """Error in configuration loading or validation."""
