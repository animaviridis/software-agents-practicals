"""Given a structured argumentation framework as input, your task here is to print out the number of attacks
(not defeats) generated."""

import sys

from argsolverdd.structured.parser import read_file
from argsolverdd.structured.argument import Arguments


rules = read_file(sys.argv[1])

arguments = Arguments(rules)
attacks = arguments.generate_attacks()

print(len(attacks))
