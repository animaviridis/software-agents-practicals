"""Given a structured argumentation framework as input, together with the preference principles and rebut
used as well as a semantics, your task is to print out the justified conclusions of the extensions.
Note that this prints out every extension ordered alphabetically and by length."""

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

# semantics in the next line can be one of "grounded","preferred", or "stable"
# returns a collection of extensions, each of which is a collection of arguments
extensions = arguments.evaluate(pa.extension, weakest_link=pa.weakest,
                                elitist=pa.elitist, restricted_rebut=pa.restr)[0]

conclusions = []  # a list of lists of the conclusions
for ext in extensions: 
        ext_conc = []  # will hold all conclusions of the extension
        for argument in ext:
                ext_conc.append(str(argument.conclusions))
        ext_conc.sort()

        conclusions.append(ext_conc)

conclusions.sort()
conclusions.sort(key=len)
print(conclusions)



