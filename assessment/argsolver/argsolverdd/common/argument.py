from argsolverdd.common.rule import Rule


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
        return all_subs

    @property
    def top_rule(self):
        return self._top_rule

    @property
    def premises(self):
        return self._top_rule.premises

    @property
    def ground_premises(self):
        prem = set(self.premises)
        for arg in self._sub_arguments:
            prem.add(arg)
            prem -= {arg.conclusions}

        return prem

    @property
    def conclusions(self):
        return self._top_rule.conclusions

    def __repr__(self):
        pn = ', '.join((p.name if isinstance(p, Argument) else str(p) for p in self.ground_premises))
        return f"{self.name}: {pn} {'->' if self.strict else '=>'} {self.conclusions}"

    def _add_sub_argument(self, arg):
        if not isinstance(arg, type(self)):
            raise TypeError(f"Argument is not an instance of {type(self)}")
        self._sub_arguments.add(arg)

    def __hash__(self):
        s = 0
        for sa in self._sub_arguments:
            s += hash(sa)
        return hash((self.top_rule, s))

    def __eq__(self, other):
        if isinstance(other, type(self)):
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

    @staticmethod
    def make_arguments(rules):
        valid_rules = [rule for rule in rules if rule.premises]
        arguments = [Argument(f"A{i+1}", rule) for i, rule in enumerate(valid_rules)]
        for argument in arguments:
            for sub_arg_candidate in arguments:
                if sub_arg_candidate == argument:
                    continue
                if sub_arg_candidate.conclusions in argument.premises:
                    argument._add_sub_argument(sub_arg_candidate)

        return arguments
