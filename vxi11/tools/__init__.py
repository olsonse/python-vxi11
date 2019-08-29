"""
This is a collection of tools that use the VXI-11 protocol to communicate with
specific instruments.  Each of these tools simplifies/organizes routine
(GPIB) commands that are used for the particular instrument.  


Tool            Instrument
----------------------------------------------------
TDS5000B        Tektronix TDS5000B oscilloscope
MS9740A         Anritsu Optical Spectrum Analyzer
MSO5074         Rigol MSO5074 Oscilloscope

A sample program that stores traces from the scope to file in a loop.

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



from . import tektronix
from . import anritsu
from . import rigol

generators = [
  anritsu,
  tektronix,
  rigol,
]

def get(idn):
  """
  Toplevel tool link generator.
  """

  idn = idn.lower()
  for g in generators:
    G = g.get(idn)
    if G: return G

  # default generator is to just return a raw vxi11.Link
  return lambda x:x
