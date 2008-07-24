"""
VXI-extension module for controlling/interacting with Tektronix TDS5000B scopes


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

from vxi11.vxi11_user import *
import time
try:
    from numpy import double
    from numpy.lib.index_tricks  import r_
except:
    print 'getCurve will not work since numpy is not found'

class TDS5000B(VXI11Link):
    """VXI-11 Link for controlling the TDS5000B."""

    def __init__(self, link=None, host=None):
        if host is not None:
            link = VXI11Client(host=host).open_link()
        VXI11Link.__init__(self,link=link)

    def waitforACQStop(self):
        """waiting (specifically for the TDS5000) to stop acquisitions."""
        while self.query('ACQUIRE:STATE?').strip() == '1':
            time.sleep(0.1);

    def getCurve(self, channel=None):
        if channel is not None:
            self.send('DATA:SOURCE %{c}s' %{'c':channel})
        self.send('DATA:ENCDG ASCII')
        self.send('WFMOUTPRE:BYT_NR 4')
        self.send('DATA:START 1')
        self.send('DATA:STOP 100000000')
        y = r_[self.query('CURVE?').strip().split(',')].astype(double)
        y0 = double(self.query('WFMOUTPRE:YOFF?').strip())
        V_dy = double(self.query('WFMOUTPRE:YMULT?').strip())
        dx = double(self.query('WFMOUTPRE:XINCR?').strip())
        y = (y - y0) * V_dy
        x = (r_[0:len(y)]) * dx
        return x,y

    def clearStatusByte(self):
        """Clear/Ignore the status byte of the TDS5000B."""
        ignore = self.query('*ESR?');

    def getStatusByte(self):
        """Get the status byte of the TDS5000B."""
        return int(self.query('*ESR?').strip())

    def printErrors(self, prefix=''):
        """Print the errors pending on the scope.  Return whether errors occurred."""
        status_byte = self.getStatusByte()
        if status_byte & TDS5000B.STATUS_BYTE.ERRS:
            print( '%(p)s:\n%(e)s' \
                %{'p':prefix, 'e':TDS5000B.getErrorsString(status_byte)})
            return True
        return False

    def getErrorsString(status_byte):
        errs = [];
        nerrs = 0;

        if status_byte & TDS5000B.STATUS_BYTE.CME:
            nerrs+=1
            errs.append('\t' + str(nerrs) + '.  command error\n')
        if status_byte & TDS5000B.STATUS_BYTE.EXE:
            nerrs+=1
            errs.append('\t' + str(nerrs) + '.  error executing command/query\n')
        if status_byte & TDS5000B.STATUS_BYTE.DDE:
            nerrs+=1
            errs.append('\t' + str(nerrs) + '.  device error\n')
        if status_byte & TDS5000B.STATUS_BYTE.QYE:
            nerrs+=1
            errs.append('\t' + str(nerrs) + '.  query/(gpib read) error\n')

        return ''.join(errs);
    getErrorsString = staticmethod(getErrorsString)

    class STATUS_BYTE:
        CME = 0x20;
        EXE = 0x10;
        DDE = 0x8;
        QYE = 0x4;
        ERRS = CME | EXE | DDE |  QYE

