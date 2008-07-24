"""
vxi11_user.py - VXI library for Python

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


import rpc
from xdrlib import Error as XDRError
import vxi11_const
from vxi11_const import *
import vxi11_type
from vxi11_type import *
import vxi11_pack

import threading


VXI11_DEFAULT_TIMEOUT   = 10000 # ms
VXI11_READ_TIMEOUT      = 2000  # ms
VXI11_LINK              = Create_LinkResp
VXI11_MAX_CLIENTS       = 256   # maximum no of unique IP addresses/clients
VXI11_NULL_READ_RESP    = 50    # vxi11_receive() return value if a query
                                # times out ON THE INSTRUMENT (and so we have
                                # to resend the query again)
VXI11_NULL_WRITE_RESP   = 51    # vxi11_send() return value if a sent command
                                # times out ON THE INSTURMENT.

RCV_END_BIT             = 0x04  # An end indicator has been read
RCV_CHR_BIT             = 0x02  # A termchr is set in flags and a character which matches termChar is transferred
RCV_REQCNT_BIT          = 0x01  # requestSize bytes have been transferred.  This includes a request size of zero.

class VXI11Exception(rpc.RPCError):
    """VXI-11 Error"""
    def __init__(self, msg=""):
        self.msg = msg
    
    def __str__(self):
        if self.msg:
            return "VXI-11 Error: %s" % self.msg
        else:
            return "VXI-11 Error "


class VXI11Error:
    errs = {
     # error    Meaning
         0   : 'No error',
         1   : 'Syntax error',
         3   : 'device not accessible',
         4   : 'invalid link identifier',
         5   : 'parameter error',
         6   : 'channel not established',
         8   : 'operation not supported',
         9   : 'out of resources',
         11  : 'device locked by another link',
         12  : 'no lock held by this link',
         15  : 'I/O timeout',
         17  : 'I/O error',
         21  : 'Invalid address',
         23  : 'abort',
         29  : 'channel already established'
    }

    def check(error=0):
        if error > 0:
            if error in VXI11Error.errs:
                raise VXI11Exception(VXI11Error.errs[error])
            else:
                raise VXI11Exception('Unknown error')
    check = staticmethod(check)


# STUB
AuthSys = rpc.SecAuthSys(0,'jupiter',103558,100,[])

from exceptions import RuntimeError

class VXI11Link(Create_LinkResp):
    def __init__(self, link=None, LinkResp=None, client=None):
        if link is not None:
            LinkResp = link
            client = link.client
        elif LinkResp is None:
            raise RuntimeError('missing VXI-11 link')
        elif client is None:
            raise RuntimeError('missing VXI-11 client')

        Create_LinkResp.__init__(self,
            error       = LinkResp.error,
            lid         = LinkResp.lid,
            abortPort   = LinkResp.abortPort,
            maxRecvSize = LinkResp.maxRecvSize
        )
        self.client = client
        self.vxi11packer = vxi11_pack.VXI11Packer()
        self.vxi11unpacker = vxi11_pack.VXI11Unpacker('')

        self.read_timeout = VXI11_READ_TIMEOUT

    def close(self):
        if self.lid in self.client.links:
            del self.client.links[self.lid]

        # I'll still try and close the link even if the link wasn't actually
        # stored in links.
        p = self.vxi11packer
        un_p = self.vxi11unpacker
        p.reset()
        p.pack_Device_Link(self.lid)
        res = self.client.call( destroy_link, p.get_buffer() )
        un_p.reset(res);
        res = un_p.unpack_Device_Error()
        VXI11Error.check(res.error)

    def send(self, cmd):
        """
           Send command(s) through the VXI-11 link to the remote device.
           cmd can either be a single string command, a list of commands, or a
           tuple of commands.
        """
        if cmd.__class__ is tuple or cmd.__class__ is list:
            # recursive call for a list of commands
            for cmd_i in cmd:
                self.send(cmd_i)
            return

        wp = Device_WriteParms(
            lid          = self.lid,
            io_timeout   = VXI11_DEFAULT_TIMEOUT,
            lock_timeout = VXI11_DEFAULT_TIMEOUT,
        )

        # We can only write (link.maxRecvSize) bytes at a time, so we sit in
        # a loop, writing a chunk at a time, until we're done. 
        p = self.vxi11packer
        un_p = self.vxi11unpacker
        while cmd != '':
            cmd_i = cmd[0:self.maxRecvSize]
            cmd = cmd[self.maxRecvSize:]

            if cmd == '': # finished
                wp.flags = 8
            else:
                wp.flags = 0

            wp.data = cmd_i

            p.reset()
            p.pack_Device_WriteParms(wp)
            res = self.client.call( device_write, p.get_buffer() )
            un_p.reset(res);
            res = un_p.unpack_Device_WriteResp()
            VXI11Error.check(res.error)

    def read(self, rqlen=None, timeout=None):
        if rqlen is None:
            # default to 1 GB? who knows?
            rqlen = 1<<30
        if timeout is None:
            timeout = self.read_timeout

        rp = Device_ReadParms(
            lid          = self.lid,
            requestSize  = rqlen,
            io_timeout   = timeout,
            lock_timeout = timeout,
            flags        = 0,
            termChar     = 0
        )

        # We can only write (link.maxRecvSize) bytes at a time, so we sit in
        # a loop, writing a chunk at a time, until we're done. 
        p = self.vxi11packer
        un_p = self.vxi11unpacker
        pos = 0
        str_list = []
        while pos < rqlen:
            rp.requestSize = rqlen - pos
            p.reset()
            p.pack_Device_ReadParms(rp)
            res = self.client.call( device_read, p.get_buffer() )
            un_p.reset(res);
            res = un_p.unpack_Device_ReadResp()
            VXI11Error.check(res.error)
            str_list.append(res.data)
            pos += len(res.data)

            if res.reason & RCV_END_BIT or res.reason & RCV_CHR_BIT:
                break

        return ''.join(str_list)

    def query(self, query_cmd, rqlen=None, timeout=None):
        """QUERY the device."""
        # note that we rely on SEND and READ to throw their own exceptions.
        self.send(query_cmd)
        return self.read(rqlen,timeout)



class VXI11Client(rpc.RPCClient):
    def __init__(self, host='localhost', port=739, sec_list=[AuthSys]):
        self.vxi11packer = vxi11_pack.VXI11Packer()
        self.vxi11unpacker = vxi11_pack.VXI11Unpacker('')
        self.links = dict()
        rpc.RPCClient.__init__(self, host, port,
                               program=DEVICE_CORE,
                               version=DEVICE_CORE_VERSION,
                               sec_list=sec_list)

    def close(self):
        """Closes the underlying socket of the RPC connection"""
        t = threading.currentThread()
        if t in self._socket:
            self._socket[t].close()
            del self._socket[t]

    next_id = 10001
    def get_unique_id():
        id = VXI11Client.next_id
        VXI11Client.next_id += 1
        return id
    get_unique_id = staticmethod(get_unique_id)

    def open_link(self, device = "inst0"):
        id = VXI11Client.get_unique_id()
        p = self.vxi11packer
        un_p = self.vxi11unpacker
        p.reset()
        p.pack_Create_LinkParms(
            Create_LinkParms(
                clientId = id,
                lockDevice = 0,
                lock_timeout = VXI11_DEFAULT_TIMEOUT,
                device=device
            )
        )
        res = self.call( create_link, p.get_buffer() )
        un_p.reset(res);
        link = un_p.unpack_Create_LinkResp()

        # check for errors, this raises exceptions on errors
        VXI11Error.check(link.error)

        self.links[link.lid] = (device,link)
        link = VXI11Link(LinkResp=link,client=self)
        return link

#############################################################

