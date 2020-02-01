"""Given a structured argumentation framework as input, your task here is to print out the number of attacks
(not defeats) generated."""

import sys

from argsolverdd.common.parser import read_file
from argsolverdd.common.argument import Argument


rules, preferences = read_file(sys.argv[1])

arguments = Argument.make_arguments(rules)
attacks = Argument.make_attacks(arguments)

print(len(attacks))
