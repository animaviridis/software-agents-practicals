"""Print out the number of extensions in which a specific argument is labelled in, out, or undec."""

from argsolverdd.common.atom import Atom
from argsolverdd.common.misc import parse_cmd_args
from argsolverdd.structured.parser import read_file
from argsolverdd.structured.argument import Arguments


pa = parse_cmd_args(add_principles=True, add_extension=True, add_target=True)
if pa.verbose:
    print(f"{'weakest' if pa.weakest else 'last'} link "
          f"{'elitist' if pa.elitist else 'democratic'} principle "
          f"with {'' if pa.restr else 'un'}restricted rebut, evaluated w.r.t. {pa.extension} extension")


rules = read_file(pa.fname)
arguments = Arguments(rules)
labellings = arguments.evaluate(pa.extension, weakest_link=pa.weakest,
                                elitist=pa.elitist, restricted_rebut=pa.restr)[1]

# target: the conclusion we want the labellings for
query = Atom(False, pa.target)
if query not in [arg.conclusions for arg in arguments]:
        raise ValueError("Target query does not match any of the arguments' conclusions")

# 1 for in, 0 for undec, -1 for out
counts = {1: 0, 0: 0, -1: 0}

for lab in labellings:
        for arg_name in lab.index:
                if arguments[arg_name].conclusions == query:
                        counts[lab[arg_name]] += 1
                        break

print((counts[1], counts[-1], counts[0]))

