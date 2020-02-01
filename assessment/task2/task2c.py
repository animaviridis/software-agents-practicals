"""Given a structured argumentation framework as input, together with the preference principles and rebut
used, your task here is to print out the number of defeats generated."""

import sys

from argsolverdd.common.parser import read_file
from argsolverdd.common.argument import Argument


rules, preferences = read_file(sys.argv[1])

arguments = Argument.make_arguments(rules)

attacks = Argument.make_attacks(arguments)

# argv[2] is one of "wd","we","ld","le",
# representing the weakest link democratic/weakest link elitist/last link democratic/last link elitist principles.
# argv[3] is "true" or "false" representing whether rebut is restricted (true) or unrestricted (false)
defeats = make_defeats(arguments, attacks, preferences, sys.argv[2], sys.argv[3])
print(len(defeats))

