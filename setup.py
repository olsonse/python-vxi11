#!/usr/bin/env python
from distutils.core import setup

import sys
import os
from os.path import join

DESCRIPTION = """
VXI-11 for python

Most was written by Spencer E. Olson <olsonse@umich.edu>
The vxi11.x file is a modified version of the one from the vxi11 for linux
package (and the author of that package borrowed it from somewhere else). 

To generate the rpc protocol for VXI-11, the vxi11.x file was parsed and
interpreted by the rpcgen.py script from 
from the newpynfs package (version 20060822).  The generated VXI-11
implementation subsequently depended on the rpc package that is also shipped
with the newpynfs package.  The newpynfs package is written by:
           Martin Murray <mmurray@deepthought.org>
and        Fred Isaman   <iisaman@citi.umich.edu>
Copyright (C) 2001 University of Michigan, Center for 
                   Information Technology Integration

I am including the rpc package from newpynfs here (but not rpcgen.py).  

"""

DIRS = [join('src','rpc'), join('src/vxi11')] # Order is important

def setup(*args, **kwargs):
  print "This just runs the setup.py file in each of the following dirs:"
  print DIRS
  print "If you want more control, say no and do it by hand"
  str = raw_input("Continue? (y/n) ")
  if (not str) or str[0] not in ['y', 'Y']:
    return
  cwd = os.getcwd()
  command = " ".join(sys.argv)
  for dir in DIRS:
    print "\n\nMoving to %s" % dir 
    os.chdir(join(cwd, dir))
    os.system("python %s" % command)
  os.chdir(cwd)

setup(
  name = "pynfs",
  version = "0.0.0", # import this?
  packages = ['rpc', 'vxi11'], 
  description = 'VXI-11 for python',
  long_description = DESCRIPTION,
  
  # These will be the same
  author = "Spencer Olson",
  author_email = "olsonse@umich.edu",
  maintainer = "Spencer Olson",
  maintainer_email = "olsonse@umich.edu",
  url = "http://github.com/olsonse/vxi11/",
  license = "GPL",
)
