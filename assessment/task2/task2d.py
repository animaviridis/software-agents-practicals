import parser
import sys

(rules,preferences)=parser.read_file(sys.argv[1])

arguments=make_arguments(rules)
attacks=make_attacks(arguments)
defeats=make_defeats(arguments,attacks,preferences,argv[2],argv[3])
#semantics in the next line can be one of "grounded","preferred", or "stable"
extensions=evaluate(arguments,defeats,argv[4]) #returns a collection of extensions, each of which is a collection of arguments

concs=[] #a list of lists of the conclusions
for ext in extensions: 
        l=[] #will hold all conclusions of the extension
        for argument in ext:
                l.add(str(argument.conclusion()))
        l.sort()        
concs.add(l)        
concs.sort()
concs.sort(key=len)
print(concs)



