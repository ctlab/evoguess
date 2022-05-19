from typing import Any


# This class using only for typings!
class Future:
    def cancel(self) -> bool:
        raise NotImplementedError

    def done(self) -> bool:
        raise NotImplementedError

    def running(self) -> bool:
        raise NotImplementedError

    def cancelled(self) -> bool:
        raise NotImplementedError

    def add_done_callback(self, fn):
        raise NotImplementedError

    def result(self, timeout=None) -> Any:
        raise NotImplementedError

    def exception(self, timeout=None) -> Exception:
        raise NotImplementedError


__all__ = [
    'Future'
]
