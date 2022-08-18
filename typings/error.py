class AlreadyRunning(Exception):
    pass


class CancelledError(Exception):
    pass


class AlreadyOpenedError(Exception):
    """The Output already opened."""
    pass


class AlreadyClosedError(Exception):
    """The Output already closed."""
    pass


class DirectoryNotExistsError(Exception):
    """The Output root directory not exists."""
    pass
