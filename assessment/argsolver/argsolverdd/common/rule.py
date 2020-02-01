from argsolverdd.common.atom import Atom
from typing import Set


class Rule:
    def __init__(self, name: str, premises: Set[Atom], conclusions: Atom, strict: bool):
        self.name = name
        self.premises = premises
        self.conclusions = conclusions
        self.strict = strict

    def __repr__(self):
        s = "=>"
        if self.strict:
            s = "->"
        p = ""
        for pr in self.premises:
            p += ", " + str(pr)
        p = p[1:]
        return "" + self.name + ":" + p + " " + s + " " + str(self.conclusions)

    def __hash__(self):
        s = 0
        if len(self.premises) > 0:
            for p in self.premises:
                s += hash(p)
        return hash((s, self.name, self.conclusions, self.strict))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.name == other.name \
            and self.conclusions == other.conclusions \
            and self.strict == other.strict \
            and self.premises == other.premises
