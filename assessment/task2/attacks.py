import sys
import networkx as nx
import matplotlib.pyplot as plt


from argsolverdd.structured.parser import read_file
from argsolverdd.structured.argument import Argument


rules, preferences = read_file(sys.argv[1])

arguments = Argument.make_arguments(rules)

attacks = set()
for a1 in arguments:
    for a2 in arguments:
        if a1 == a2:
            continue

        if a1.rebuts(a2) or a1.undercuts(a2):
            attacks.add((a1.name, a2.name))

print(len(attacks))


fig, ax = plt.subplots()
graph = nx.DiGraph()
argnames = [a.name for a in arguments]
graph.add_nodes_from(argnames)
graph.add_edges_from(attacks)
nx.draw(graph, ax=ax, with_labels=argnames, node_color='lightblue')
ax.set_title(f"Rebuts and undercuts from {sys.argv[1]}")
plt.show()
