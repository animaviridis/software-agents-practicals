"""Given a structured argumentation framework as input, your task here is to print out the number of strict
and defeasible arguments which can be generated. You should base your answer on the file task2a.py,
modifying it as needed."""

import sys

from argsolverdd.common.parser import read_file
from argsolverdd.common.argument import Arguments


rules, preferences = read_file(sys.argv[1])

arguments = Arguments(rules, preferences)

strict = 0
defeasible = 0

for a in arguments:
    if a.strict:
        strict += 1
    else:
        defeasible += 1

print(strict, defeasible)
