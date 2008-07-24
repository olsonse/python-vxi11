#!/usr/bin/python
"""
A very simple demonstration of the VXI-11 library and a link to the TDS5000B
scope.

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

# make sure that you include the path to the rpc and vxi11 packages.
import sys, os
sys.path.append( os.path.join(os.path.pardir, 'src') )

from vxi11.tools import TDS5000B
from vxi11 import VXI11Client

_mpl_ = False
try:
    from pylab import *
    _mpl_ = True
except:
    print 'sad to not have matplotlib'

def main():
    # all these links to the same scope can be used to do basic vxi-11
    # send/read/query.  The TDS5000B links include a bit more functionality,
    # such as downloading a trace from the TDS5000B scope.  You could of
    # course have accomplished the same thing with the generic link, but this
    # makes it easier.

    # vxi-11 link to the TDS5000B. Includes extra functionality for this
    # scope.
    scope = TDS5000B(host='rbscope')
    status_byte = int(scope.query('*ESR?').strip())
    try:
        x,y = scope.getCurve()
        if _mpl_:
            plot (x,y)
            show()
    except:
        print 'I guess we do not have numpy available.'


    # vxi-11 link to some device (this same scope in this case)
    link = VXI11Client(host='rbscope').open_link()
    status_byte = int(link.query('*ESR?').strip())


    # vxi-11 link to the TDS5000B just like above.  Reinterprets the link
    # specifically as one to the TDS5000B.  This is the same link (link id) as
    # the one that we reinterpret.
    scope2 = TDS5000B(link=link)
    status_byte = int(scope2.query('*ESR?').strip())
    try:
        x,y = scope.getCurve()
    except:
        print 'I guess we do not have numpy available.'

    raw_input('Press enter to quit')


if __name__ == "__main__":
    main()

