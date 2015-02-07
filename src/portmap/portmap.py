# Port mapper interface

# Program number, version and (fixed!) port number
PMAP_PROG = 100000
PMAP_VERS = 2
PMAP_PORT = 111

# Procedure numbers
PMAPPROC_NULL = 0                       # (void) -> void
PMAPPROC_SET = 1                        # (mapping) -> bool
PMAPPROC_UNSET = 2                      # (mapping) -> bool
PMAPPROC_GETPORT = 3                    # (mapping) -> unsigned int
PMAPPROC_DUMP = 4                       # (void) -> pmaplist
PMAPPROC_CALLIT = 5                     # (call_args) -> call_result

# A mapping is (prog, vers, prot, port) and prot is one of:

IPPROTO_TCP = 6
IPPROTO_UDP = 17

# A pmaplist is a variable-length list of mappings, as follows:
# either (1, mapping, pmaplist) or (0).

# A call_args is (prog, vers, proc, args) where args is opaque;
# a call_result is (port, res) where res is opaque.


class PortMapperPacker(Packer):

    def pack_mapping(self, mapping):
        prog, vers, prot, port = mapping
        self.pack_uint(prog)
        self.pack_uint(vers)
        self.pack_uint(prot)
        self.pack_uint(port)

    def pack_pmaplist(self, list):
        self.pack_list(list, self.pack_mapping)

    def pack_call_args(self, ca):
        prog, vers, proc, args = ca
        self.pack_uint(prog)
        self.pack_uint(vers)
        self.pack_uint(proc)
        self.pack_opaque(args)


class PortMapperUnpacker(Unpacker):

    def unpack_mapping(self):
        prog = self.unpack_uint()
        vers = self.unpack_uint()
        prot = self.unpack_uint()
        port = self.unpack_uint()
        return prog, vers, prot, port

    def unpack_pmaplist(self):
        return self.unpack_list(self.unpack_mapping)

    def unpack_call_result(self):
        port = self.unpack_uint()
        res = self.unpack_opaque()
        return port, res


class PartialPortMapperClient:

    def addpackers(self):
        self.packer = PortMapperPacker()
        self.unpacker = PortMapperUnpacker('')

    def Set(self, mapping):
        return self.make_call(PMAPPROC_SET, mapping, \
                self.packer.pack_mapping, \
                self.unpacker.unpack_uint)

    def Unset(self, mapping):
        return self.make_call(PMAPPROC_UNSET, mapping, \
                self.packer.pack_mapping, \
                self.unpacker.unpack_uint)

    def Getport(self, mapping):
        return self.make_call(PMAPPROC_GETPORT, mapping, \
                self.packer.pack_mapping, \
                self.unpacker.unpack_uint)

    def Dump(self):
        return self.make_call(PMAPPROC_DUMP, None, \
                None, \
                self.unpacker.unpack_pmaplist)

    def Callit(self, ca):
        return self.make_call(PMAPPROC_CALLIT, ca, \
                self.packer.pack_call_args, \
                self.unpacker.unpack_call_result)


class TCPPortMapperClient(PartialPortMapperClient, RawTCPClient):

    def __init__(self, host):
        RawTCPClient.__init__(self, \
                host, PMAP_PROG, PMAP_VERS, PMAP_PORT)


class UDPPortMapperClient(PartialPortMapperClient, RawUDPClient):

    def __init__(self, host):
        RawUDPClient.__init__(self, \
                host, PMAP_PROG, PMAP_VERS, PMAP_PORT)


class BroadcastUDPPortMapperClient(PartialPortMapperClient, \
                                   RawBroadcastUDPClient):

    def __init__(self, bcastaddr):
        RawBroadcastUDPClient.__init__(self, \
                bcastaddr, PMAP_PROG, PMAP_VERS, PMAP_PORT)





# Simple test program -- dump local portmapper status

def test():
    pmap = UDPPortMapperClient('')
    list = pmap.Dump()
    list.sort()
    for prog, vers, prot, port in list:
        print prog, vers,
        if prot == IPPROTO_TCP: print 'tcp',
        elif prot == IPPROTO_UDP: print 'udp',
        else: print prot,
        print port


# Test program for broadcast operation -- dump everybody's portmapper status

def testbcast():
    import sys
    if sys.argv[1:]:
        bcastaddr = sys.argv[1]
    else:
        bcastaddr = '<broadcast>'
    def rh(reply, fromaddr):
        host, port = fromaddr
        print host + '\t' + repr(reply)
    pmap = BroadcastUDPPortMapperClient(bcastaddr)
    pmap.set_reply_handler(rh)
    pmap.set_timeout(5)
    replies = pmap.Getport((100002, 1, IPPROTO_UDP, 0))
