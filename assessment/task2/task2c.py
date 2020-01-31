import parser
import sys

(rules,preferences)=parser.read_file(sys.argv[1])

arguments=make_arguments(rules)
attacks=make_attacks(arguments)
#argv[2] is one of "wd","we","ld","le", representing the weakest link democratic/weakest link elitist/last link democratic/last link elitist principles.
#argv[3] is "true" or "false" representing whether rebut is restricted (true) or unrestricted (false)
defeats=make_defeats(arguments,attacks,preferences,sys.argv[2],sys.argv[3])
print(len(defeats))

