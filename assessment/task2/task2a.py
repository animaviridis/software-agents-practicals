import parser
import sys

(rules,preferences)=parser.read_file(sys.argv[1])

arguments=make_arguments(rules)
strict=0
defeasible=0
for a in arguments:
        if a.strict():
                strict+=1
        else:
                defeasible+=1

print(strict,defeasible)

