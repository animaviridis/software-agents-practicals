import sys
import networkx as nx
import matplotlib.pyplot as plt


from argsolverdd.structured.parser import read_file
from argsolverdd.structured.argument import Arguments


rules = read_file(sys.argv[1])

arguments = Arguments(rules)

argnames = [a.name for a in arguments]


def plot_graph(data, axis, title=None, color='lightblue'):
    graph = nx.DiGraph()
    graph.add_nodes_from(argnames)
    dnames = [tuple(d.name for d in dd) for dd in data]
    graph.add_edges_from(dnames)
    print(f"\n{len(dnames)} {title}:\n{dnames}")
    nx.draw(graph, ax=axis, with_labels=argnames, node_color=color)
    axis.set_title(title)


fig, ax = plt.subplots(2, 1)
plot_graph(arguments.generate_attacks(), axis=ax[0], title="Attacks", color='lightblue')
plot_graph(arguments.generate_defeats(), axis=ax[1], title="Defeats", color='lightgreen')
fig.subplots_adjust(hspace=0.3, left=0.2, right=0.8)
plt.show()
