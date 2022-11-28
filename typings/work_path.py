import os


class WorkPath:
    def __init__(self, *dirs: str, root: str = '.'):
        self.root = os.path.abspath(root)
        self.base = os.path.join(self.root, *dirs)

        if not os.path.exists(self.base):
            os.makedirs(self.base, exist_ok=True)

    def to_path(self, *dirs: str) -> 'WorkPath':
        return WorkPath(*dirs, root=self.base)

    def to_file(self, filename: str) -> str:
        return os.path.join(self.base, filename)

    def __str__(self) -> str:
        return self.base


__all__ = [
    'WorkPath'
]
