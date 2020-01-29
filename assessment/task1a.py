"""Given an abstract argument framework file, print out list of the stable extensions (lists), sorted alphabetically."""

import sys
import copy
from collections import defaultdict

from parser_abstract import read_file

arguments, rules = read_file(sys.argv[1] if len(sys.argv) > 1 else 'aaf.aaf')  # TODO: parser

attacks = defaultdict(lambda: [])
for rule in rules:
    attacks[rule[0]].append(rule[1])

attackers = attacks.keys()

arg_dict = {a: 0 for a in arguments}
extensions = []

for start_arg in attackers:
    print(f"\nStarting from {start_arg}")
    ad = copy.deepcopy(arg_dict)
    ad[start_arg] = 1
    contradiction = False

    decided = [start_arg]

    for arg in decided:
        val = ad[arg]
        print(f"Considering {arg}={val}")
        if arg not in attackers:
            continue

        for r2 in attacks[arg]:
            print(arg, r2)

            if ad[r2] == val:
                contradiction = True
                print("Contradiction")
                break

            if ad[r2] == 0:
                ad[r2] = - val
                print(f'{r2} = {"IN" if val == -1 else "OUT"}')
                decided.append(r2)

    if all(ad.values()) and not contradiction:
        extensions.append([arg for arg, val in ad.items() if val == 1])

print(f"\nExtensions: {extensions}")
