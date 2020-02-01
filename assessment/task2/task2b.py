import sys

from argsolverdd.common.parser import read_file
from argsolverdd.common.argument import Argument


rules, preferences = read_file(sys.argv[1])

arguments = Argument.make_arguments(rules)

attacks = set()
for a1 in arguments:
    for a2 in arguments:
        if a1 == a2:
            continue

        if a1.rebuts(a2) or a1.undercuts(a2):
            attacks.add((a1, a2))

print(len(attacks))
