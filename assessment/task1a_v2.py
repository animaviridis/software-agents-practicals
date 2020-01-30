import sys
import numpy as np
from pandas import DataFrame
import networkx as nx
import matplotlib.pyplot as plt

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
    outs_ = attacks.index[attacks.loc[arg_] == 1]
    attacks.loc[outs_, :] = 0
    return outs_


ins = list(get_ins())
outs = []

for arg in ins:
    print(f"Considering argument {arg}")
    label_dict[arg] = 1
    outs.extend(cleanup(arg))

    ins.extend(set(get_ins()) - set(ins))
    print(ins)

for arg in outs:
    label_dict[arg] = -1

print(f"\nGrounded extension - ins: {list(get_ins())}")
print(f"Outs: {outs}")
print(f"Undec: {[a for a, v, in label_dict.items() if not v]}")


fig, ax = plt.subplots()
graph = nx.DiGraph()
graph.add_edges_from(rules)
colors = {-1: 'crimson', 0: 'lightslategrey', 1: 'limegreen'}
nx.draw(graph, ax=ax,
        with_labels={a: a for a in arguments_sorted},
        node_color=[colors[label_dict[a]] for a in graph.nodes])
ax.set_title("Argument framework graph", fontsize=16)
plt.show()
