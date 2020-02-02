from argsolverdd.common.rule import Rule, Rules
from argsolverdd.common.atom import Atom
from argsolverdd.common.misc import NameDict


class Argument:
    def __init__(self, name: str, top_rule: Rule):
        self.name = name
        self._top_rule = top_rule
        self._sub_arguments = set()

    @property
    def direct_sub_arguments(self):
        return self._sub_arguments

    @property
    def all_sub_arguments(self):
        all_subs = set(self.direct_sub_arguments)
        for sub in self.direct_sub_arguments:
            for subsub in sub.all_sub_arguments:
                all_subs.add(subsub)
        all_subs.add(self)

        return set(all_subs)

    @property
    def top_rule(self):
        return self._top_rule

    @property
    def all_rules(self):
        r = [self._top_rule]

        for sub in self._sub_arguments:
            r.extend(sub.all_rules)

        return Rules(r)

    @property
    def all_defeasible_rules(self):
        return Rules([r for r in self.all_rules if not r.strict])

    @property
    def last_defeasible_rules(self):
        if not self._top_rule.strict:
            return Rules([self._top_rule])

        def_rules = []
        for sub in self._sub_arguments:
            def_rules.extend(sub.last_defeasible_rules)

        return Rules(def_rules)

    def get_rules_to_compare(self, weakest_link=True):
        if weakest_link:
            return self.all_defeasible_rules
        return self.last_defeasible_rules

    @property
    def premises(self):
        if not self._sub_arguments:
            return self._top_rule.premises or {self._top_rule.conclusions}

        prem = set()
        for sub in self._sub_arguments:
            for p in sub.premises:
                prem.add(p)
        return prem

    @property
    def conclusions(self):
        return self._top_rule.conclusions

    def __repr__(self):
        if self._sub_arguments:
            prem = ', '.join((s.name for s in self._sub_arguments))
        else:
            prem = ''

        return f"{self.name}: {prem} {'->' if self.strict else '=>'} {self.conclusions}"

    def add_sub_argument(self, arg):
        if not isinstance(arg, type(self)):
            raise TypeError(f"Argument is not an instance of {type(self)}")
        self._sub_arguments.add(arg)

    def __hash__(self):
        s = 0
        for sa in self._sub_arguments:
            s += hash(sa)
        return hash((self.top_rule, s))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        if self.top_rule != other.top_rule:
            return False
        for s in self.all_sub_arguments:
            if s not in other.all_sub_arguments:
                return False
        return True

    @property
    def strict(self):
        return self._top_rule.strict

    def rebuts(self, other, restricted_rebut=False):
        if not isinstance(other, type(self)):
            raise TypeError(f"{other} is not an instance of {type(self)}")

        for osub in other.all_sub_arguments:
            if restricted_rebut:
                if osub.strict:
                    continue  # in restricted rebut, the attacked argument's top rule must be defeasible -> return False

            if self.conclusions.contrary(osub.conclusions):
                return True

        return False

    def undercuts(self, other):
        if not isinstance(other, type(self)):
            raise TypeError(f"{other} is not an instance of {type(self)}")

        for osub in other.all_sub_arguments:
            if osub.top_rule.strict:
                continue
            if self.conclusions.contrary(Atom(False, osub.top_rule.name)):
                return True
        return False

    def preferred_to(self, other, weakest_link=True, elitist=True):
        """Return True if an argument is preferred (>=) to another one, False otherwise"""

        r1, r2 = (a.get_rules_to_compare(weakest_link=weakest_link) for a in (self, other))
        return r1.preferred_to(r2, elitist=elitist)


class Arguments(NameDict):
    def __init__(self, rules):
        super().__init__(self.make_arguments(rules))
        self.rules = rules

    @staticmethod
    def make_arguments(rules):
        arguments = [Argument(f"A{i+1}", rule) for i, rule in enumerate(rules)]
        for argument in arguments:
            for sub_arg_candidate in arguments:
                if sub_arg_candidate == argument:
                    continue
                if sub_arg_candidate.conclusions in argument.top_rule.premises:
                    argument.add_sub_argument(sub_arg_candidate)

        return arguments

    def generate_attacks(self, restricted_rebut=False):
        attacks = set()
        for a1 in self:
            for a2 in self:
                if a1 == a2:
                    continue

                if a1.rebuts(a2, restricted_rebut=restricted_rebut) or a1.undercuts(a2):
                    attacks.add((a1, a2))

        return attacks

    def generate_defeats(self, weakest_link=True, elitist=True, restricted_rebut=False):
        attacks = self.generate_attacks(restricted_rebut=restricted_rebut)

        defeats = set()
        for a1, a2 in attacks:
            if a1.preferred_to(a2, weakest_link=weakest_link, elitist=elitist):
                defeats.add((a1, a2))

        return defeats

