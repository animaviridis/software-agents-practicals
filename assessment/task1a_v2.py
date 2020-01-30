import sys
import numpy as np
from pandas import DataFrame

from parser_abstract import read_file


arguments, rules = read_file(sys.argv[1] if len(sys.argv) > 1 else 'aaf.aaf')  # TODO: parser
la = len(arguments)
arguments_sorted = sorted(arguments)

attacks = DataFrame(np.zeros((la, la), int), index=arguments_sorted, columns=arguments_sorted)

for rule in rules:
    attacks.loc[rule[0], rule[1]] = 1


print(f"\nAttack matrix:\n{attacks}")

label_dict = {a: 0 if attacks.loc[:, a].any() else 1 for a in arguments_sorted}

print(f"\nInitial labellings:\n{label_dict}")


def get_ins():
    return attacks.index[attacks.sum(axis=0) == 0]


def cleanup(arg_):
    attacks.loc[attacks.loc[arg_] == 1, :] = 0


ins = list(get_ins())

for arg in ins:
    print(f"Considering argument {arg}")
    cleanup(arg)

    ins.extend(set(ins) - set(get_ins()))


print(f"\nGrounded extension: {get_ins()}")
