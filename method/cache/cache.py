from .parts import *


class Cache:
    def __init__(self, *args):
        self.best = {}
        self.active = {}
        self.canceled = {}
        self.estimated = {}
        self.state = State(*args)

    def reset_best(self):
        self.best = {}

    def update_best(self, item):
        self.best = self.estimated.get(str(item), self.best)
