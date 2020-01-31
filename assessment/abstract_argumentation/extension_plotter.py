import networkx as nx
import matplotlib.pyplot as plt


class ExtensionPlotter(object):
    def __init__(self, rules):
        self.graph = nx.DiGraph()
        self.graph.add_edges_from(rules)
        self.graph_colors = {-1: 'crimson', 0: 'lightslategrey', 1: 'limegreen'}

    def plot(self, labels, title=None):
        fig, ax = plt.subplots()
        nx.draw(self.graph, ax=ax,
                with_labels={a: a for a in self.graph.nodes},
                node_color=[self.graph_colors[labels[a]] for a in self.graph.nodes])
        ax.set_title(title or "Argument framework graph", fontsize=16)
        plt.show()
