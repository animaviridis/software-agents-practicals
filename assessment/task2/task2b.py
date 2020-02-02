"""Given a structured argumentation framework as input, your task here is to print out the number of attacks
(not defeats) generated."""

from argsolverdd.common.misc import parse_cmd_args
from argsolverdd.structured.parser import read_file
from argsolverdd.structured.argument import Arguments


pa = parse_cmd_args()
rules = read_file(pa.fname)

arguments = Arguments(rules)
attacks = arguments.generate_attacks()

print(len(attacks))
