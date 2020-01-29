"""Given an abstract argument framework file, print out list of the stable extensions (lists), sorted alphabetically."""

import sys
import copy

from parser_abstract import read_file

arguments, rules = read_file('aaf.aaf')  # TODO: read_file(sys.argv[1])

arg_dict = {a: 0 for a in arguments}
extensions = []

for start_arg in arguments:
    print(f"\nStarting from {start_arg}")
    ad = copy.deepcopy(arg_dict)
    ad[start_arg] = 1

    n_changes = 1
    decided = [start_arg]

    for arg in decided:
        val = ad[arg]
        print(f"Considering {arg}={val}")

        n_changes = 0

        for rule in rules:
            if rule[0] == arg:
                print(rule)
                r2 = rule[1]

                if ad[r2] == val:
                    print("contradiction")
                    break

                if ad[r2] == 0:
                    ad[r2] = - val
                    print(f'{r2} = {"IN" if val == -1 else "OUT"}')
                    decided.append(r2)

    if all(ad.values()):
        extensions.append([arg for arg, val in ad.items() if val == 1])

print(f"\nExtensions: {extensions}")
