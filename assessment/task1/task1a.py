import sys

from ground_extensor import Extensor

ext = Extensor.from_file(sys.argv[1], verbose=False)
ext.ground()
print(sorted(ext.label_ins))
