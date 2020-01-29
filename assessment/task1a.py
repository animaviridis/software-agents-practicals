"""Given an abstract argument framework file, print out list of the stable extensions (lists), sorted alphabetically."""

import sys
import copy
from collections import defaultdict

from parser_abstract import read_file

arguments, rules = read_file(sys.argv[1] if len(sys.argv) > 1 else 'aaf.aaf')  # TODO: parser

attackers_dict = defaultdict(lambda: [])
attacked_dict = defaultdict(lambda: [])

for rule in rules:
    attackers_dict[rule[0]].append(rule[1])
    attacked_dict[rule[1]].append(rule[0])

attackers = attackers_dict.keys()
attacked = attacked_dict.keys()
attack_free = [a for a in attackers if a not in attacked]


def evaluate(ad, abort=True):
    decided = [arg for arg, val in ad.items() if val]

    for arg in decided:
        val = ad[arg]
        print(f"Considering {arg}={val}")
        if arg not in attackers:
            continue

        for r2 in attackers_dict[arg]:
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

grounded_ext = evaluate(arg_dict, False) or []
print(f"\nGrounded extension: {grounded_ext}")

stable_ext = []


for start_arg in [arg for arg, val in arg_dict.items() if not val and arg in attackers]:
    print(f"\nStarting from {start_arg}")
    current_ad = copy.deepcopy(arg_dict)
    current_ad[start_arg] = 1

    ext = evaluate(current_ad)
    if ext:
        print(f"New extension: {ext}")
        stable_ext.append(ext)

print(f"\nStable extensions: {stable_ext}")
