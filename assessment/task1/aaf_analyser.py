import sys

from argsolverdd.abstract.stable_extensor import StableExtensor
from argsolverdd.abstract.extension_plotter import ExtensionPlotter

fname = sys.argv[1]
arguments, rules = StableExtensor.read_file(fname)
ext = StableExtensor(arguments, rules)
plotter = ExtensionPlotter(rules)

ext.ground()
print(f"\nGrounded extension: {sorted(ext.label_ins)}")
plotter.plot(ext.labels, f"AAF: grounded extension ({ext.label_ins})")


def plot_ext(stable=True):
    p = "Stable" if stable else "Preferred"
    ext_list, lab_list = ext.get_preferred_extensions(require_stable=stable)

    print(f"\n{p} extensions: {ext_list}")
    for i, lab in enumerate(lab_list):
        plotter.plot(lab, title=f"{p} extension [{i+1}/{len(lab_list)}]: {lab.index[lab==1].values}")


plot_ext(True)
plot_ext(False)
