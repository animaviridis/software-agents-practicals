"""Given a structured argumentation framework as input, your task here is to print out the number of attacks
(not defeats) generated."""

import sys

from argsolverdd.structured.parser import read_file
from argsolverdd.structured.argument import Arguments


rules, preferences = read_file(sys.argv[1])

arguments = Arguments(rules, preferences)
attacks = arguments.generate_attacks()

print(len(attacks))
