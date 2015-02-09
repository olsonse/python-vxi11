"""
An implementation of the VXI-11 protocol for python.

This is not necessarily the most accurate representation of the VXI-11
specification, but it is simple.

The thread-safe nature (or lack thereof) has not been explored.  Deviations of
this implementation to the VXI-11 specification have not been investigated. 

Requires python 2.3

Written by Spencer E. Olson <olsonse@umich.edu>
Copyright (C) 2008 Spencer E. Olson


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

from vxi11_user import *

import tools
from tools import *
