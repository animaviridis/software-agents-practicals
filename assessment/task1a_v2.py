import sys
import numpy as np
from pandas import DataFrame, Series
import networkx as nx
import matplotlib.pyplot as plt

from parser_abstract import read_file


class Extensor(object):
    class Contradiction(ValueError):
        pass

    def __init__(self, file_name, verbose=False):
        arguments, rules = read_file(file_name)
        self.arguments = sorted(arguments)
        self._attacks = self.make_attacks_matrix(rules)
        self._labels = Series({a: 0 if self._attacks.loc[:, a].any() else 1 for a in self.arguments})

        self.assumed_ins = []

        self.graph = nx.DiGraph()
        self.graph.add_edges_from(rules)
        self.graph_colors = {-1: 'crimson', 0: 'lightslategrey', 1: 'limegreen'}

        self.print = print if verbose else lambda *args: None

    @property
    def attacks(self):
        return self._attacks

    @property
    def labels(self):
        return self._labels

    def _get_by_label(self, lab):
        return list(self.labels.index[self.labels == lab])

    @property
    def label_ins(self):
        return self._get_by_label(1)

    @property
    def label_outs(self):
        return self._get_by_label(-1)

    @property
    def label_undec(self):
        return self._get_by_label(0)

    @property
    def stable(self):
        return len(self.label_undec) == 0

    def make_attacks_matrix(self, rules):
        la = len(self.arguments)
        attacks = DataFrame(np.zeros((la, la), int), index=self.arguments, columns=self.arguments)

        for rule in rules:
            attacks.loc[rule[0], rule[1]] = 1

        return attacks

    def get_ins(self):
        return self.attacks.index[self.attacks.sum(axis=0) == 0]

    def _clear_defeated(self, arg):
        outs = self.attacks.index[self.attacks.loc[arg] == 1]
        if self.assumed_ins:
            contr = [a for a in outs if a in self.assumed_ins]
            if contr:
                raise self.Contradiction(f"Contradiction: argument {contr[0]}, assumed to be IN, re-evaluated to OUT")

        self.labels[outs] = -1
        self.attacks.loc[outs, :] = 0

    def ground(self, new_args: list = None):
        ins = new_args or list(self.get_ins())

        for arg in ins:
            self.print(f"Considering argument {arg}")
            self.labels[arg] = 1
            self._clear_defeated(arg)

            ins.extend(set(self.get_ins()) - set(ins))

        self.print(f"\nIns: {self.label_ins}")
        self.print(f"Outs: {self.label_outs}")
        self.print(f"Undec: {self.label_undec}")

    def assume_in(self, arg):
        if self.labels[arg]:
            raise ValueError(f"Argument '{arg}' is not UNDEC")
        self.print(f"\nAssuming argument '{arg}' to be IN")
        self.assumed_ins.append(arg)

        try:
            self.ground([arg])
        except self.Contradiction as e:
            self.print(e)
            return False
        else:
            return True

    def plot(self, title=None):
        fig, ax = plt.subplots()
        nx.draw(self.graph, ax=ax,
                with_labels={a: a for a in self.graph.nodes},
                node_color=[self.graph_colors[self.labels[a]] for a in self.graph.nodes])
        ax.set_title(title or "Argument framework graph", fontsize=16)
        plt.show()


if __name__ == '__main__':
    f = sys.argv[1] if len(sys.argv) > 1 else 'aaf.aaf'
    ext = Extensor(f, True)
    ext.ground()
    print(f"\nGrounded extension: {sorted(ext.label_ins)}")
    ext.plot()

    if not ext.stable:
        if ext.assume_in(ext.label_undec[0]):
            ext.plot()
