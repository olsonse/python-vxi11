import sys
import os
from os.path import join, split
cwd = os.getcwd()
if True or cwd not in sys.path:
    head, tail = split(cwd)
    dirs = [ join(head, 'rpc'),
             join(head),
             #cwd,
             ]
    sys.path[1:1] = dirs
