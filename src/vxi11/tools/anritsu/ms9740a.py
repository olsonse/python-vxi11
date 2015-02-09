"""
VXI-extension module for controlling/interacting with Anritsu MS9740A OSA


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

import vxi11
import time
try:
  from numpy import double
  from numpy import r_
except:
  print 'getCurve will not work since numpy is not found'

class MS9740A(vxi11.Link):
    """VXI-11 Link for controlling the MS9740A."""
    IDN = 'ms9740a'

    def __init__(self, link=None, host=None):
        if host is not None:
            link = vxi11.Client(host=host).open_link()
        super(MS9740A,self).__init__(link=link)
