
'''
---From https://project-haystack.org/doc/docHaystack/Kinds#grid
Grid is a two dimensional tabular data type. Grids are essentially a list of dicts.
However grids may include grid level and column level meta data which is modeled as
a dict. Grids are the fundamental unit of data exchange over the HTTP API

This should do the trick
https://github.com/clarsen/pyhaystack/blob/master/pyhaystack/client/ops/his.py
https://pint.readthedocs.io/en/stable/
https://github.com/widesky/hszinc
'''

import hszinc
import pyhaystack

