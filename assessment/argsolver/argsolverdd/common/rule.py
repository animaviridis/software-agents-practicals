from typing import Set

from argsolverdd.common.atom import Atom
from argsolverdd.common.misc import NameDict


class Rule:
    def __init__(self, name: str, premises: Set[Atom], conclusions: Atom, strict: bool):
        self.name = name
        self.premises = premises
        self.conclusions = conclusions
        self.strict = strict
        self.preferred_to = set()

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

    def __ge__(self, other):
        if not isinstance(other, type(self)):
            raise TypeError(f"Cannot compare Rule with {type(other)}")

        if self.strict and not other.strict:
            return True

        if other.strict and not self.strict:
            return False

        return self not in other.preferred_to

    @staticmethod
    def assign_preferences(ruleset, pref_dict):
        for rule in ruleset:
            rule.preferred_to = pref_dict[rule]


class Rules(NameDict):
    def __init__(self, rules):
        super(Rules, self).__init__(rules)

    def _compare_elitist(self, other) -> bool:
        """There is some rule in set R1 which is preferred (>=) to all rules in ser R2

        Return True if the current is preferred to the other, False otherwise.
        """

        for r1 in self:
            if all(r1 >= r2 for r2 in other):
                return True
        return False

    def _compare_democratic(self, other) -> bool:
        """For every rule r1 in set R1, there is a rule r2 in set R2 which is less preferred (r1 >= r2)

        Return True if the current is preferred to the other, False otherwise.
        """

        for r1 in self:
            if not any(r1 >= r2 for r2 in other):
                return False
        return True

    def preferred_to(self, other, elitist=True):
        if elitist:
            return self._compare_elitist(other)
        else:
            return self._compare_democratic(other)

