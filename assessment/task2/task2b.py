import parser
import sys

(rules,preferences)=parser.read_file(sys.argv[1])

arguments=make_arguments(rules)
attacks=make_attacks(arguments)
print(len(attacks))

