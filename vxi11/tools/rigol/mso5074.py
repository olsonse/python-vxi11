"""
VXI-extension module for controlling/interacting with Rigol MSO5074
Oscilloscope.  It seems that this is also the DS1000Z Digital Oscilloscope--not
to certain how consistent Rigol is about naming their hardware.

Written by Spencer E. Olson <olsonse@umich.edu>

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
  import numpy as np
  from numpy import double
  from numpy import r_
except:
  print('getCurve will not work since numpy is not found')

def assert_channel(channel):
  assert channel in [1,2,3,4], 'invalid channel'

class MSO5074(vxi11.Link):
  """
  VXI-11 Link for controlling the Rigol MSO5074 (DS1000Z Digital Oscilloscope).
  """
  model = 'mso5074'

  def __init__(self, link=None, host=None):
    if host is not None:
      link = vxi11.Client(host=host).open_link()
    super(MSO5074,self).__init__(link=link)

  def getdata(self,channel):
    assert_channel(channel)
    DM = ':WAV:DATA? CHAN{}'.format(channel)
    return np.frombuffer(self.query(DM), 'B')

  def getspan(self, channel):
    assert_channel(channel)
    DC = 'DC{}?'.format(channel)
    xi,xf,N = [ float(i) for i in self.query(DC).decode().strip().split(',') ]
    N = int(N)
    return xi,xf,N

  def getCurve(self,channel):
    y       = self.getdata(channel)
    xi,xf,N = self.getspan(channel)
    return r_[xi:xf:(1j*N)], y
