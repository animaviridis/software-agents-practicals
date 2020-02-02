from lark import Lark, Transformer
from argsolverdd.common.rule import Rule, Rules
from argsolverdd.common.atom import Atom

grammar = r"""
NEG: "!"
NUMBER: /[0-9_]\w*/
NUMBERSTRING: /[a-zA-Z0-9_]\w*/
STRICT: "->"
DEFEASIBLE: "=>"
COMMENT: /#[^\n]*/

ruleset: (arule|priority)*
arule: NUMBERSTRING ":" prem (STRICT|DEFEASIBLE) atom 
prem: [atom ("," atom)*]
conc: atom
priority: NUMBERSTRING ("<=") NUMBERSTRING 
atom: NEG? NUMBERSTRING

%import common.WS
%ignore WS
"""

parser = Lark(grammar, start='ruleset')


class MyTransformer(Transformer):
    def ruleset(self, args):
        rules = set()
        priorities = set()
        for a in args:
            if type(a) == Rule:
                # print(a)
                rules.add(a)
            else:
                priorities.add(a)

        rh = {}
        preferred_to = {}  # preferred_to[x] means contents are preferred to x
        for r in rules:
            rh[r.name] = r
            preferred_to[r] = set()
        for p in priorities:
            preferred_to[rh[p[1]]].add(rh[p[0]])

        Rule.assign_preferences(rules, preferred_to)
        return Rules(rules)

    def priority(self, args):
        return str(args[1]), str(args[0])

    def arule(self, args):
        name = str(args[0])
        prems = args[1]
        if prems == None:
            prems = set()
        strict = (args[2].type == "STRICT")
        conc = args[3]
        return Rule(name, prems, conc, strict)

    def atom(self, args):
        if args[0].type == "NEG":
            return Atom(True, str(args[1]))
        else:
            return Atom(False, str(args[0]))

    def prem(self, args):
        return set(args)


def read_file(filename):
    with open(filename, 'r') as myfile:
        return MyTransformer().transform(parser.parse(myfile.read()))
