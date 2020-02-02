from copy import deepcopy

from argsolverdd.abstract.ground_extensor import Extensor


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

    def __enter__(self):
        self.back_up()

    def __exit__(self, *args, **kwargs):
        self.roll_back()

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

        self.print(f"\nAssuming argument '{arg}' to be IN")
        self.labels[arg] = 1
        self.assumed_ins.append(arg)

        try:
            self.ground()
        except self.Contradiction as e:
            self.print(e)
            return False
        else:
            return True

    def get_stable_extensions(self):
        return self.get_preferred_extensions(require_stable=True)

    def get_preferred_extensions(self, require_stable=False, ext_list=None, lab_list=None):
        ext_list = ext_list or []
        lab_list = lab_list or []

        if self.stable or not require_stable:
            se = sorted(self.label_ins)
            if se not in ext_list:
                ext_list.append(se)
                lab_list.append(deepcopy(self.labels))

        if not self.stable:
            for arg in self.label_undec:
                with self:
                    if self.assume_in(arg):
                        ext_list, lab_list = self.get_preferred_extensions(require_stable=require_stable,
                                                                           ext_list=ext_list, lab_list=lab_list)

        if require_stable:
            return ext_list, lab_list

        # for preferred extensions only - stable are already complete
        return self.reduce_extensions(ext_list, lab_list)

    @staticmethod
    def reduce_extensions(ext_list, lab_list):
        """reduce the preferred extensions w.r.t. set inclusion"""

        ext_set_list = [set(ext) for ext in ext_list]

        final_ext_list = []
        final_lab_list = []

        for i, ext in enumerate(ext_set_list):
            ext_set_sublist = ext_set_list[:i] + ext_set_list[i + 1:]
            if any(ext.issubset(other_ext) for other_ext in ext_set_sublist):
                continue

            final_ext_list.append(ext_list[i])
            final_lab_list.append(lab_list[i])

        return final_ext_list, final_lab_list
