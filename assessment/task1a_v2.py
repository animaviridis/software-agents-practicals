import sys
import numpy as np
import pandas as pd
import copy

from parser_abstract import read_file

arguments, rules = read_file(sys.argv[1] if len(sys.argv) > 1 else 'aaf.aaf')  # TODO: parser
la = len(arguments)
arguments_sorted = sorted(arguments)

attacks = pd.DataFrame(np.zeros((la, la), int), index=arguments_sorted, columns=arguments_sorted)

for rule in rules:
    attacks.loc[rule[0], rule[1]] = 1


print(f"\nAttack matrix:\n{attacks}")


label_dict = {a: 0 if attacks.loc[:, a].any() else 1 for a in arguments_sorted}
print(f"\nInitial labellings:\n{label_dict}")

