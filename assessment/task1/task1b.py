"""Analyse an abstract argumentation framework and output arguments belonging to the grounded extension."""

from argsolverdd.common.misc import parse_cmd_args
from argsolverdd.abstract.ground_extensor import Extensor

pa = parse_cmd_args()

ext = Extensor.from_file(pa.fname, verbose=pa.verbose)
ext.ground()
print(sorted(ext.label_ins))
