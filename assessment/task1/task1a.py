"""Analyse an abstract argumentation framework and output arguments belonging to its stable extensions."""

import sys

from stable_extensor import StableExtensor


if len(sys.argv) < 2:
    raise RuntimeError("No data file provided")

ext = StableExtensor.from_file(sys.argv[1], verbose=False)
print(ext.get_stable_extensions())
