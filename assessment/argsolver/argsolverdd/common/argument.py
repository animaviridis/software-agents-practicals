from argsolverdd.common.rule import Rule
from argsolverdd.common.atom import Atom


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
            body = f"{prem} {'->' if self.strict else '=>'} "
        else:
            body = ''

        return f"{self.name}: {body}{self.conclusions}"

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

    def rebuts(self, other):
        if not isinstance(other, type(self)):
            raise TypeError(f"{other} is not an instance of {type(self)}")

        for osub in other.all_sub_arguments:
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


class Arguments(dict):
    def __init__(self, rules, preferences=None):
        super().__init__({a.name: a for a in self.make_arguments(rules)})
        self.rules = {r.name: r for r in rules}
        self.preferences = preferences or {}

    def __repr__(self):
        return str(set(self.values()))

    def __iter__(self):
        yield from self.values()

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

    def generate_attacks(self):
        attacks = set()
        for a1 in self.values():
            for a2 in self.values():
                if a1 == a2:
                    continue

                if a1.rebuts(a2) or a1.undercuts(a2):
                    attacks.add((a1, a2))

        return attacks

    def generate_defeats(self, weakest_link=True, elitist=True, restricted_rebut=False):
        attacks = self.generate_attacks()

        return []

