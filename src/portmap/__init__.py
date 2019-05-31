"""
An implementation of the Portmapper client for python.

Written by Spencer E. Olson <olsonse@umich.edu>
Copyright (C) 2015 Spencer E. Olson


This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License. 

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
"""

from .client import Client
from .portmap_const import *

from .portmap_type import \
  pmap2_mapping as mapping, \
  pmap2_call_args as call_args


def get_address( host, prog, vers, prot, port=None ):
  if port:
    return (host,port)
  pmap = Client(host)
  port = pmap.getport( mapping( prog, vers, prot, 0 ) )
  del pmap
  return (host,port)
