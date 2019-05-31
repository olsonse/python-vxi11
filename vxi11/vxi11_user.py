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


import rpc, portmap
from xdrlib import Error as XDRError
from . import vxi11_const
from .vxi11_const import *
from . import vxi11_type
from .vxi11_type import *
from . import vxi11_pack

import threading, six


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


class VXI11Error(object):
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

  @staticmethod
  def check(error=0):
    if error > 0:
      if error in VXI11Error.errs:
        raise VXI11Exception(VXI11Error.errs[error])
      else:
        raise VXI11Exception('Unknown error')



class Link(Create_LinkResp):
  def __init__(self, link=None, LinkResp=None, client=None):
    if link is not None:
      LinkResp = link
      client = link.client
    elif LinkResp is None:
      raise RuntimeError('missing VXI-11 link')
    elif client is None:
      raise RuntimeError('missing VXI-11 client')

    super(Link,self).__init__(
      error       = LinkResp.error,
      lid         = LinkResp.lid,
      abortPort   = LinkResp.abortPort,
      maxRecvSize = LinkResp.maxRecvSize
    )
    self.client = client
    self.p = vxi11_pack.VXI11Packer()
    self.un_p = vxi11_pack.VXI11Unpacker(b'')

    self.read_timeout = VXI11_READ_TIMEOUT

  def _make_call( self, procedure, data, packer, unpacker, timeout=None ):
    self.p.reset()
    packer( data )
    xid = self.client.send_call( self.client.pipe, procedure, self.p.get_buffer() )
    header, data = self.client.pipe.listen( xid, timeout )
    self.un_p.reset( data )
    res = unpacker()
    VXI11Error.check(res.error)
    return res


  def close(self, **kw):
    if self.lid in self.client.links:
      del self.client.links[self.lid]

    # I'll still try and close the link even if the link wasn't actually
    # stored in links.
    res = self._make_call( destroy_link, self.lid,
                           self.p.pack_Device_Link,
                           self.un_p.unpack_Device_Error, **kw )

  def send(self, cmd):
    """
    Send command(s) through the VXI-11 link to the remote device.
    cmd can either be a single string command, a list of commands, or a
    tuple of commands.
    """
    if cmd.__class__ in [tuple,list]:
      # recursive call for a list of commands
      for cmd_i in cmd:
        self.send(cmd_i)
      return

    # ensure the user's data is encoded as bytes
    if isinstance(cmd, six.string_types):
      cmd = cmd.encode()

    wp = Device_WriteParms(
      lid          = self.lid,
      io_timeout   = VXI11_DEFAULT_TIMEOUT,
      lock_timeout = VXI11_DEFAULT_TIMEOUT,
    )

    # We can only write (link.maxRecvSize) bytes at a time, so we sit in
    # a loop, writing a chunk at a time, until we're done.
    while cmd != b'':
      cmd_i = cmd[0:self.maxRecvSize]
      cmd = cmd[self.maxRecvSize:]

      if cmd == b'': # finished
        wp.flags = 8
      else:
        wp.flags = 0

      wp.data = cmd_i

      res = self._make_call( device_write, wp,
                             self.p.pack_Device_WriteParms,
                             self.un_p.unpack_Device_WriteResp,
                             timeout=1.5*VXI11_DEFAULT_TIMEOUT )
      assert len(cmd_i) == res.size, 'link.send: Could not write data'

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

    # We can only read (unknown) bytes at a time, so we sit in
    # a loop, reading a chunk at a time, until we're done.
    pos = 0
    str_list = list()
    while pos < rqlen:
      rp.requestSize = rqlen - pos

      res = self._make_call( device_read, rp,
                             self.p.pack_Device_ReadParms,
                             self.un_p.unpack_Device_ReadResp,
                             timeout=1.5*timeout )
      str_list.append(res.data)
      pos += len(res.data)

      if res.reason & RCV_END_BIT or res.reason & RCV_CHR_BIT:
        break

    return b''.join(str_list)

  def query(self, query_cmd, rqlen=None, timeout=None):
    """QUERY the device."""
    # note that we rely on SEND and READ to throw their own exceptions.
    self.send(query_cmd)
    return self.read(rqlen,timeout)

  def _simple_generic_proc(self, proc, unpacker=None):
    if unpacker is None:
      unpacker = self.un_p.unpack_Device_Error
    return self._make_call( proc,
      Device_GenericParms(
        lid          = self.lid,
        flags        = 0,
        io_timeout   = VXI11_DEFAULT_TIMEOUT,
        lock_timeout = VXI11_DEFAULT_TIMEOUT,
      ),
      self.p.pack_Device_GenericParms,
      unpacker,
      timeout=1.5*VXI11_DEFAULT_TIMEOUT,
    )

  def status(self):
    return self._simple_generic_proc(
      device_trigger,self.un_p.unpack_Device_ReadStbResp
    ).stb
  def trigger(self):
    self._simple_generic_proc( device_trigger )
  def clear(self):
    self._simple_generic_proc( device_clear )
  def remote(self):
    self._simple_generic_proc( device_remote )
  def local(self):
    self._simple_generic_proc( device_local )



EP = lambda x :  b''
EU = lambda x : None


class Client(rpc.Client):
  def __init__(self, host='localhost', port=None):
    super(Client,self).__init__( DEVICE_CORE, DEVICE_CORE_VERSION )
    address = portmap.get_address(
      host, DEVICE_CORE, DEVICE_CORE_VERSION, portmap.IP_TCP, port
    )

    self.pipe = self.connect( address )
    self.p    = vxi11_pack.VXI11Packer()
    self.un_p = vxi11_pack.VXI11Unpacker(b'')
    self.links = dict()

  def __del__(self):
    self.close()
  def close(self):
    """Closes the underlying socket of the RPC connection"""
    self.pipe._s.close()

  def _make_call( self, procedure, data, packer=EP, unpacker=EU, timeout=None ):
    self.p.reset()
    packer( data )
    xid = self.send_call( self.pipe, procedure, self.p.get_buffer() )
    header, data = self.pipe.listen( xid, timeout )
    self.un_p.reset( data )
    return unpacker()


  next_id = 10001
  @staticmethod
  def get_unique_id():
    id = Client.next_id
    Client.next_id += 1
    return id

  def open_link(self, device = b"inst0", autoid=True):
    res = self._make_call(
      create_link,
      Create_LinkParms(
        clientId = self.get_unique_id(),
        lockDevice = 0,
        lock_timeout = VXI11_DEFAULT_TIMEOUT,
        device=device,
      ),
      self.p.pack_Create_LinkParms,
      self.un_p.unpack_Create_LinkResp,
      timeout=VXI11_DEFAULT_TIMEOUT,
    )

    # check for errors, this raises exceptions on errors
    VXI11Error.check(res.error)

    self.links[res.lid] = (device,res)
    LinkClass = Link
    link = Link(LinkResp=res,client=self)
    if autoid:
      from . import tools # delayed to allow complete loading
      return tools.get( link.query('*IDN?'.encode()).decode() )(link)
    return link
