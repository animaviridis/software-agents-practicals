"""Given an abstract argument framework file, print out list of the stable extensions (lists), sorted alphabetically."""

import sys
import copy
from collections import defaultdict

from parser_abstract import read_file

arguments, rules = read_file(sys.argv[1] if len(sys.argv) > 1 else 'aaf.aaf')  # TODO: parser

attacks = defaultdict(lambda: [])
attacked = []
for rule in rules:
    attacks[rule[0]].append(rule[1])
    attacked.append(rule[1])

attackers = attacks.keys()
attack_free = [a for a in attackers if a not in attacked]


def evaluate(ad, abort=True):
    decided = [arg for arg, val in ad.items() if val]

    for arg in decided:
        val = ad[arg]
        print(f"Considering {arg}={val}")
        if arg not in attackers:
            continue

        for r2 in attacks[arg]:
            print(arg, r2)

            if ad[r2] == val and val == 1:
                ad[r2] = 0
                print("Contradiction")
                if abort:
                    break

            elif ad[r2] == 0:
                ad[r2] = - val
                print(f'{r2} = {"IN" if val == -1 else "OUT"}')
                decided.append(r2)

    if all(ad.values()):
        return [arg for arg, val in ad.items() if val == 1]


arg_dict = {a: int(a in attack_free) for a in arguments}

grounded_ext = evaluate(arg_dict) or []
print(f"\nGrounded extension: {grounded_ext}")

extensions = []


for start_arg in attackers:
    print(f"\nStarting from {start_arg}")
    current_ad = copy.deepcopy(arg_dict)
    current_ad[start_arg] = 1

    ext = evaluate(current_ad)
    if ext:
        print(f"New extension: {ext}")
        extensions.append(ext)

print(f"\nExtensions: {extensions}")
