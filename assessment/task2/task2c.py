"""Given a structured argumentation framework as input, together with the preference principles and rebut
used, your task here is to print out the number of defeats generated."""

from argsolverdd.common.misc import parse_cmd_args
from argsolverdd.structured.parser import read_file
from argsolverdd.structured.argument import Arguments

# prepare arguments
# argv[2] is one of "wd", "we", "ld", "le",
# representing the weakest link democratic/weakest link elitist/last link democratic/last link elitist principles.
# argv[3] is "true" or "false" representing whether rebut is restricted (true) or unrestricted (false)


pa = parse_cmd_args(add_principles=True)

if pa.verbose:
    print(f"{'weakest' if pa.weakest else 'last'} link "
          f"{'elitist' if pa.elitist else 'democratic'} principle "
          f"with {'' if pa.restr else 'un'}restricted rebut")

# parse the file
rules = read_file(pa.fname)

# generate arguments, attacks, and defeats
arguments = Arguments(rules)
defeats = arguments.generate_defeats(weakest_link=pa.weakest, elitist=pa.elitist, restricted_rebut=pa.restr)

print(len(defeats))

