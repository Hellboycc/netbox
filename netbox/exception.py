class NetboxException(Exception):
    """An exception that Netbox can handle and show to the users."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

    def format_message(self) -> str:
        return self.message


class AuthenticationFailed(NetboxException):
    """Raised if a connection authenticate failed."""


class CommandException(NetboxException):
    """Raised if a command execute failed."""
