import parser
import sys
from atom import Atom

(rules,preferences)=parser.read_file(sys.argv[1])

arguments=make_arguments(rules)
attacks=make_attacks(arguments)
defeats=make_defeats(arguments,attacks,preferences,argv[2],argv[3])
#semantics in the next line can be one of "grounded","preferred", or "stable"
labellings=label(arguments,defeats,argv[4]) 
#argv[5] is the conclusion we want the labellings for
query=Atom(argv[5])
in=0
out=0
undec=0
for lab in labellings:
        if lab.conc_in(query)):
                in+=1
        elif lab.conc_out(query)):
                out+=1
        else:
                undec+=1
print((in,out,undec))



