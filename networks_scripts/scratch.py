import os
import pandas as pd
import csv
import numpy as np
import math
#

#
# d1 = {'A': 1, 'B': 2, 'C': 3}
# d2 = {'A': 1, 'B': 2, 'C': 3}
#
# ds = [d1, d2]
# d = {}
# for k in d1.iterkeys():
#     d[k] = tuple(d[k] for d in ds)
#
# print(d)


a = [('A', 1), ('B', 2), ('C', 3), ('D', 4), ('E', 5)]

factor = int(math.ceil(0.4*len(a)))
print(factor)
top = sorted(a, key = lambda x: x[1], reverse = True)[:factor]
print(top)