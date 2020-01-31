import numpy as np
from pandas import DataFrame, Series

from parser_abstract import read_file


class Extensor(object):
    def __init__(self, arguments, rules, verbose=False):
        self.arguments = sorted(arguments)
        self.attacks = self.make_attacks_matrix(rules)
        self.labels = Series({a: 0 if self.attacks.loc[:, a].any() else 1 for a in self.arguments})

        self.print = print if verbose else lambda *args: None

    @staticmethod
    def read_file(file_name):
        return read_file(file_name)

    @staticmethod
    def from_file(file_name, **kwargs):
        arguments, rules = Extensor.read_file(file_name)
        return Extensor(arguments, rules, **kwargs)

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

    def make_attacks_matrix(self, rules):
        la = len(self.arguments)
        attacks = DataFrame(np.zeros((la, la), int), index=self.arguments, columns=self.arguments)

        for rule in rules:
            attacks.loc[rule[0], rule[1]] = 1

        return attacks

    def get_ins(self):
        return self.attacks.index[self.attacks.sum(axis=0) == 0]

    def _check_contradictions(self, *args, **kwargs):
        pass

    def _clear_defeated(self, arg):
        outs = self.attacks.index[self.attacks.loc[arg] == 1]

        self._check_contradictions(outs)

        self.labels[outs] = -1
        self.attacks.loc[outs, :] = 0
        return outs

    def ground(self):
        ins = self.label_ins or self.get_ins()

        for arg in ins:
            self.print(f"Considering argument {arg}")
            self.labels[arg] = 1
            self._clear_defeated(arg)

            ins.extend(set(self.get_ins()) - set(ins))

        self.print(f"\nIns: {self.label_ins}")
        self.print(f"Outs: {self.label_outs}")
        self.print(f"Undec: {self.label_undec}")

