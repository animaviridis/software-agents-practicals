"""Analyse an abstract argumentation framework and output arguments belonging to its stable extensions."""

from argsolverdd.common.misc import parse_cmd_args
from argsolverdd.abstract.stable_extensor import StableExtensor


pa = parse_cmd_args()

ext = StableExtensor.from_file(pa.fname, verbose=pa.verbose)
print(ext.get_stable_extensions())
