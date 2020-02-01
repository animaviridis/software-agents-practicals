import sys

from argsolverdd.abstract.stable_extensor import StableExtensor
from argsolverdd.abstract.extension_plotter import ExtensionPlotter

fname = sys.argv[1]
arguments, rules = StableExtensor.read_file(fname)
ext = StableExtensor(arguments, rules)
plotter = ExtensionPlotter(rules)

ext.ground()
print(f"\nGrounded extension: {sorted(ext.label_ins)}")
plotter.plot(ext.labels, f"AAF: grounded extension ({ext.label_ins}])")
