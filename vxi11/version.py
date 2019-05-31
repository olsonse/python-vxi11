#!/usr/bin/env python3
# vim: ts=2:sw=2:tw=80:nowrap

from subprocess import Popen, PIPE
import re, os
from os import path

THIS_DIR = path.dirname(__file__)
VERSION_FILE = path.join( THIS_DIR, 'VERSION' )
DEFAULT_PREFIX = 'python-vxi11'

__all__ = [
  'VERSION', 'version_tuple', 'version', 'version_number', 'compatible',
]

TAG_FMT = '(?P<name>(-[^0-9]|[^-])*)-' \
          '(?P<version>[0-9]+(\\.[0-9]+)*)' \
          '(-(?P<increment>[0-9]+)-g(?P<hash>[0-9a-fA-F]+))?$'

def match_version(v):
  try:
    return re.match(TAG_FMT, v).groupdict()
  except:
    return dict(name=DEFAULT_PREFIX, version='0.0.0', increment=None, hash=None)

def version_tuple(v):
  try:
    m = match_version(v)
    t = tuple( int(i) for i in m['version'].split('.') )
    if m['increment']:
      t += ( int(m['increment']), m['hash'] )
    return t
  except:
    return (-1,-1,-1,v)


def read_file_version():
  f = open(VERSION_FILE)
  v = f.readline()
  f.close()
  return v.strip()


def version():
  try:
    args = {'cwd' : THIS_DIR }
    devnull = open(os.devnull, 'w')
    p = Popen(['git', 'describe'], stdout=PIPE, stderr=devnull, **args)
    out,err = p.communicate()
    if p.returncode:
      raise RuntimeError('no version defined?')
    return out.strip().decode()
  except:
    # failover is to try VERSION_FILE instead
    try:
      return read_file_version()
    except:
      return DEFAULT_PREFIX + '-0.0.0'

def version_number(v=None):
  if v is None:
    v = version()
  return v[len(DEFAULT_PREFIX)+1:]


def compatible(v0, v1):
  v0 = version_tuple(v0)
  v1 = version_tuple(v1)
  return v0[:2] == v1[:2]

def write_version_file(v=None):
  if v is None:
    v = version()
  f = open( VERSION_FILE, 'w' )
  f.write(v)
  f.close()



VERSION = version()


if __name__ == '__main__':
  import sys, argparse
  p = argparse.ArgumentParser()
  p.add_argument( '--save', action='store_true',
    help='Store version to '+VERSION_FILE)
  p.add_argument( '--read-file-version', action='store_true',
    help='Read the version stored in '+VERSION_FILE)
  p.add_argument( '--version-number', action='store_true',
    help='Show parsed version number (minus prefix)')
  p.add_argument( '--version-filepath', action='store_true',
    help='Show path to VERSION file')
  args = p.parse_args()

  v = version()
  if args.save:
    write_version_file(v)
  if args.read_file_version:
    v = read_file_version()

  if args.version_filepath:
    print(VERSION_FILE)

  if args.version_number:
    print(version_number(v))
  else:
    print(v)
