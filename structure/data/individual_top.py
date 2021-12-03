from structure.individual import Individual


class IndividualsTop:
    def __init__(self, size: int = 10, bound: int = None):
        self.top = []
        self.keys = []
        self.size = size
        self.bound = bound
        self.max = float('inf')

    def _find(self, target: Individual, key):
        for i, individual in enumerate(self.top):
            if individual.value > target.value:
                return i
        return len(self.top)

    def check(self, individual: Individual) -> bool:
        if self.bound and len(individual.backdoor) < self.bound:
            return False

        key = str(individual.backdoor)
        if key in self.keys:
            return False

        if individual.value > self.max:
            if len(self.top) < self.size:
                self.keys.append(key)
                self.top.append(individual)
                self.max = individual.value
                return True
            return False

        pos = self._find(individual, key)
        if pos >= self.size:
            return False

        self.keys.insert(pos, key)
        self.top.insert(pos, individual)
        if len(self.top) > self.size:
            self.top.pop(-1)
            self.keys.pop(-1)
            self.max = self.top[-1].value
        return True

    def list(self):
        return self.top
