"""Given a structured argumentation framework as input, together with the preference principles and rebut
used, your task here is to print out the number of defeats generated."""


from argparse import ArgumentParser

from argsolverdd.common.parser import read_file
from argsolverdd.common.argument import Argument

# prepare arguments
# argv[2] is one of "wd", "we", "ld", "le",
# representing the weakest link democratic/weakest link elitist/last link democratic/last link elitist principles.
# argv[3] is "true" or "false" representing whether rebut is restricted (true) or unrestricted (false)

parser = ArgumentParser()
parser.add_argument('fname', type=str, help="Data file name")
parser.add_argument('principle', type=str, choices=['wd', 'we', 'ld', 'le'],
                    help='preference principles: weakest/last and democratic/elitist')
parser.add_argument('restr', type=str, choices=['true', 'false'])

parsed_args = parser.parse_args()
weakest = parsed_args.principle[0] == 'w'
elitist = parsed_args.principle[1] == 'e'
restr = parsed_args.restr == 'true'


# parse the file
rules, preferences = read_file(parsed_args.fname)

# generate arguments, attacks, and defeats
arguments = Argument.make_arguments(rules)
attacks = Argument.make_attacks(arguments)

defeats = Argument.make_defeats(arguments, attacks, preferences=preferences,
                                weakest_link=weakest, elitist=elitist, restricted_rebut=restr)

print(len(defeats))

