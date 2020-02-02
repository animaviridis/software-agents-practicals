from typing import Set
from collections import defaultdict

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


class Rules(NameDict):
    def __init__(self, rules, preferences=None):
        super(Rules, self).__init__(rules)
        preferences = preferences or defaultdict(lambda: set())
        for rule, pref in preferences.items():
            self[rule].preferred_to = pref

    def _compare_elitist(self, ruleset1, ruleset2) -> bool:
        """There is some rule in set R1 which is preferred (>=) to all rules in ser R2

        Return True if ruleset1 is preferred to ruleset2, False otherwise.
        """

        for r1 in ruleset1:
            pref1 = self[r1.name].preferred_to
            if all(r2 in pref1 for r2 in ruleset2):
                return True
        return False

    def _compare_democratic(self, ruleset1, ruleset2) -> bool:
        """For every rule r1 in set R1, there is a rule r2 in set R2 which is less preferred (r1 >= r2)

        Return True if ruleset1 is preferred to ruleset2, False otherwise.
        """

        for r1 in ruleset1:
            pref1 = self[r1.name].preferred_to
            if not any(r2 in pref1 for r2 in ruleset2):
                return False
        return True

    def preferred_to(self, ruleset1, ruleset2, elitist=True):
        if elitist:
            return self._compare_elitist(ruleset1, ruleset2)
        else:
            return self._compare_democratic(ruleset1, ruleset2)

