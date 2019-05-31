# vim: et:sw=2:ts=2:tw=80:nowrap
"""
client.py - Portmapper client library for Python

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

if __name__ == '__main__':
  import sys
  sys.path.append('..')

import rpc
from xdrlib import Error as XDRError
from . import portmap_const
from .portmap_const import *
from . import portmap_type
from .portmap_type import *
from .import portmap_pack

# A pmaplist is a variable-length list of mappings, as follows:
# either (1, mapping, pmaplist) or (0).

# A call_args is (prog, vers, proc, args) where args is opaque;
# a call_result is (port, res) where res is opaque.

EP = lambda x :  ''
EU = lambda x : None


class Client(rpc.Client):
  def __init__(self, host):
    super(Client,self).__init__( PMAP_PROGRAM, PMAP_V2 )
    self.pipe = self.connect( (host, PMAP_PORT) )
    self.p    = portmap_pack.PORTMAPPacker()
    self.un_p = portmap_pack.PORTMAPUnpacker('')

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

  def null(self, **kw):
    return self._make_call( PMAP2_NULL, None, **kw )

  def set(self, mapping, **kw):
    return self._make_call( PMAP2_SET, mapping,
                            self.p.pack_pmap2_mapping,
                            self.un_p.unpack_bool, **kw )

  def unset(self, mapping, **kw):
    return self._make_call( PMAP2_UNSET, mapping,
                            self.p.pack_pmap2_mapping,
                            self.un_p.unpack_bool, **kw )

  def getport(self, mapping, **kw):
    return self._make_call( PMAP2_GETPORT, mapping,
                            self.p.pack_pmap2_mapping,
                            self.un_p.unpack_uint, **kw )

  def dump(self, **kw):
    L = self._make_call( PMAP2_DUMP, None, EP,
                         self.un_p.unpack_pmap2_dump_result, **kw ).list
    R = list()
    while L:
      L = L[0]
      R.append( L.map )
      L = L.next
    return R

  def callit(self, call_args, **kw):
    return self._make_call( PMAP2_CALLIT, call_args,
                            self.p.pack_pmap2_call_args,
                            self.un_p.unpack_pmap2_call_result, **kw )



def test():
  """
  Simple test program -- dump local portmapper status
  """
  import six
  pmap = Client('localhost')
  L = pmap.dump()
  L.sort()
  for m in L:
    six.print_(m.prog, m.vers, end=' ')
    if m.prot == IP_TCP:
      six.print_('tcp', end=' ')
    elif m.prot == IP_UDP:
      six.print_('udp', end=' ')
    else:
      six.print_(m.prot, end=' ')
    six.print_(m.port)

if __name__ == '__main__':
  test()
