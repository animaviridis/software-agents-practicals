from argsolverdd.common.misc import parse_cmd_args
from argsolverdd.structured.parser import read_file
from argsolverdd.structured.argument import Arguments


pa = parse_cmd_args(add_principles=True, add_extension=True)
if pa.verbose:
    print(f"{'weakest' if pa.weakest else 'last'} link "
          f"{'elitist' if pa.elitist else 'democratic'} principle "
          f"with {'' if pa.restr else 'un'}restricted rebut, evaluated w.r.t. {pa.extension} extension")


rules = read_file(pa.fname)

arguments = Arguments(rules)
defeats = arguments.generate_defeats(weakest_link=pa.weakest, elitist=pa.elitist, restricted_rebut=pa.restr)


# semantics in the next line can be one of "grounded","preferred", or "stable"
# returns a collection of extensions, each of which is a collection of arguments
extensions = evaluate(arguments, defeats, pa.extension)

conclusions = []  # a list of lists of the conclusions
for ext in extensions: 
        l = []  # will hold all conclusions of the extension
        for argument in ext:
                l.append(str(argument.conclusion()))
        l.sort()

        conclusions.append(l)

conclusions.sort()
conclusions.sort(key=len)
print(conclusions)



