from argsolverdd.common.rule import *


class Argument:
    def __init__(self, toprule, subarguments):
        self.toprule = toprule
        self.subarguments = subarguments

    def __hash__(self):
        s = 0
        for sa in self.subarguments:
            s += hash(sa)
        return hash((self.toprule, s))

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return False
        if self.toprule != other.toprule:
            return False
        for s in self.subarguments:
            if s not in other.subarguments:
                return False
        return True

    def strict(self):
        pass
