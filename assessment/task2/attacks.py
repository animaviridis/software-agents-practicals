import networkx as nx
import matplotlib.pyplot as plt

from argsolverdd.common.misc import parse_cmd_args
from argsolverdd.structured.parser import read_file
from argsolverdd.structured.argument import Arguments

pa = parse_cmd_args(add_principles=True, add_extension=True)

rules = read_file(pa.fname)

arguments = Arguments(rules)

argnames = [a.name for a in arguments]


def plot_graph(data, axis, title=None, color='lightblue', plot_disconnected=False):
    graph = nx.DiGraph()
    if plot_disconnected:
        graph.add_nodes_from(argnames)
    dnames = [tuple(d.name for d in dd) for dd in data]
    graph.add_edges_from(dnames)
    print(f"\n{len(dnames)} {title}:\n{dnames}")
    nx.draw(graph, ax=axis, with_labels=argnames, node_color=color)
    axis.set_title(title)


fig, ax = plt.subplots(2, 1)
plot_graph(arguments.generate_attacks(restricted_rebut=False), axis=ax[0], title="Attacks", color='lightblue')
plot_graph(arguments.generate_defeats(restricted_rebut=pa.restr, weakest_link=pa.weakest, elitist=pa.elitist),
           axis=ax[1], title="Defeats", color='lightgreen')
fig.subplots_adjust(hspace=0.3, left=0.2, right=0.8)
plt.show()
