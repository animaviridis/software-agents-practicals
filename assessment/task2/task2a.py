"""Given a structured argumentation framework as input, your task here is to print out the number of strict
and defeasible arguments which can be generated. You should base your answer on the file task2a.py,
modifying it as needed."""

from argsolverdd.common.misc import parse_cmd_args
from argsolverdd.structured.parser import read_file
from argsolverdd.structured.argument import Arguments

pa = parse_cmd_args()
rules = read_file(pa.fname)

arguments = Arguments(rules)

strict = 0
defeasible = 0

for a in arguments:
    if a.strict:
        strict += 1
    else:
        defeasible += 1

print(strict, defeasible)
