#!/usr/bin/env python3
from distutils.command.build_py import build_py as _build_py
from glob import glob
from setuptools import setup, find_packages

import sys
import os
from os.path import join
from subprocess import Popen, PIPE

sys.path.insert(0, 'rpc')
import xdrgen

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

THIS_DIR = os.path.dirname( __file__ )

def version_stuff():
  """Gets version info and saves version file"""
  p = Popen(['./vxi11/version.py', '--version-filepath',
                                   '--version-number',
                                   '--save'], stdout=PIPE)
  o, e = p.communicate()
  VERSION_FILE, VERSION_NUMBER = o.decode().split()
  return VERSION_FILE, VERSION_NUMBER

VERSION_FILE, VERSION_NUMBER = version_stuff()


VERSION_FILE = os.path.relpath(VERSION_FILE, THIS_DIR)
MANIFEST_in = join(THIS_DIR, 'MANIFEST.in')
f = open(MANIFEST_in, 'w')
f.write('include {}\n'.format(VERSION_FILE))
f.write('graft rpc\n')
f.write('graft portmap\n')
f.write('graft vxi11\n')
f.close()

class build_py(_build_py):
  """Specialized Python source builder that scans for .x files"""
  def build_packages (self):
    # A copy from _build_py, with a call to expand_xdr added
    for package in self.packages:
      package_dir = self.get_package_dir(package)
      self.expand_xdr(package_dir)
    super(build_py, self).build_packages()

  def expand_xdr(self, dir):
    print('expanding xdr in ', dir)
    cwd = os.getcwd()
    xdr_files = glob(os.path.join(dir, "*.x"))
    for f in xdr_files:
      # Can conditionalize this
      # XXX need some way to pass options here
      xdrgen.run(f)

try:
  setup(
    name = 'vxi11',
    version = VERSION_NUMBER.partition('-g')[0],
    packages = ['rpc', 'portmap', 'vxi11'],
    cmdclass = {'build_py': build_py},
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

finally:
  os.unlink(MANIFEST_in)
