from copy import deepcopy

from abstract_argumentation.ground_extensor import Extensor


class Backup(object):
    def __init__(self, extensor):
        self.attacks = deepcopy(extensor.attacks)
        self.labels = deepcopy(extensor.labels)
        self.assumed_ins = deepcopy(extensor.assumed_ins)


class StableExtensor(Extensor):
    class Contradiction(ValueError):
        pass

    def __init__(self, *args, **kwargs):
        super(StableExtensor, self).__init__(*args, **kwargs)

        self.assumed_ins = []
        self._backup = []

    @property
    def stable(self):
        return len(self.label_undec) == 0

    def _check_contradictions(self, outs):
        if self.assumed_ins:
            contr = [a for a in outs if a in self.assumed_ins]
            if contr:
                raise self.Contradiction(f"Contradiction: argument {contr[0]}, assumed to be IN, re-evaluated to OUT")

    def back_up(self):
        self._backup.append(Backup(self))

    def roll_back(self):
        if not self._backup:
            raise RuntimeError("No backup available")

        self.print("Roll back")

        backup = self._backup.pop()
        self.attacks = backup.attacks
        self.labels = backup.labels
        self.assumed_ins = backup.assumed_ins

    def assume_in(self, arg):
        if self.labels[arg]:
            raise ValueError(f"Argument '{arg}' is not UNDEC")

        self.labels[arg] = 1
        self.print(f"\nAssuming argument '{arg}' to be IN")
        self.assumed_ins.append(arg)

        try:
            self.ground([arg])
        except self.Contradiction as e:
            self.print(e)
            return False
        else:
            return True

    def get_stable_extensions(self, stable_ext=None):
        stable_ext = stable_ext or []

        if self.stable:
            se = sorted(self.label_ins)
            if se not in stable_ext:
                stable_ext.append(se)
        else:
            for arg in self.label_undec:
                self.back_up()
                if self.assume_in(arg):
                    stable_ext = self.get_stable_extensions(stable_ext)
                self.roll_back()

        return stable_ext

