"""Analyse an abstract argumentation framework and output arguments belonging to the grounded extension."""

import sys

from ground_extensor import Extensor


if len(sys.argv) < 2:
    raise RuntimeError("No data file provided")

ext = Extensor.from_file(sys.argv[1], verbose=False)
ext.ground()
print(sorted(ext.label_ins))
