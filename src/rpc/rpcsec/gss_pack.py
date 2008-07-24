# Generated by rpcgen.py from gss.x on Thu Jul 10 17:06:52 2008
import gss_const as const
import gss_type as types
import xdrlib
from xdrlib import Error as XDRError

class nullclass(object):
    pass

class GSSPacker(xdrlib.Packer):
    pack_hyper = xdrlib.Packer.pack_hyper
    pack_string = xdrlib.Packer.pack_string
    pack_opaque = xdrlib.Packer.pack_opaque
    pack_int = xdrlib.Packer.pack_int
    pack_double = xdrlib.Packer.pack_double
    pack_float = xdrlib.Packer.pack_float
    pack_unsigned = xdrlib.Packer.pack_uint
    pack_quadruple = xdrlib.Packer.pack_double
    pack_uhyper = xdrlib.Packer.pack_uhyper
    pack_uint = xdrlib.Packer.pack_uint
    pack_bool = xdrlib.Packer.pack_bool
    def pack_rpc_gss_proc_t(self, data):
        if data not in [const.RPCSEC_GSS_DATA, const.RPCSEC_GSS_INIT, const.RPCSEC_GSS_CONTINUE_INIT, const.RPCSEC_GSS_DESTROY]:
            raise XDRError, 'value=%s not in enum rpc_gss_proc_t' % data
        self.pack_int(data)

    def pack_rpc_gss_service_t(self, data):
        if data not in [const.rpc_gss_svc_none, const.rpc_gss_svc_integrity, const.rpc_gss_svc_privacy]:
            raise XDRError, 'value=%s not in enum rpc_gss_service_t' % data
        self.pack_int(data)

    def pack_rpc_gss_cred_vers_1_t(self, data):
        if data.gss_proc is None:
            raise TypeError, 'data.gss_proc == None'
        self.pack_rpc_gss_proc_t(data.gss_proc)
        if data.seq_num is None:
            raise TypeError, 'data.seq_num == None'
        self.pack_uint(data.seq_num)
        if data.service is None:
            raise TypeError, 'data.service == None'
        self.pack_rpc_gss_service_t(data.service)
        if data.handle is None:
            raise TypeError, 'data.handle == None'
        self.pack_opaque(data.handle)

    def pack_rpc_gss_cred_t(self, data):
        if data.vers is None:
            raise TypeError, 'data.vers == None'
        self.pack_uint(data.vers)
        if data.vers == const.RPCSEC_GSS_VERS_1:
            if data.rpc_gss_cred_vers_1_t is None:
                raise TypeError, 'data.rpc_gss_cred_vers_1_t == None'
            self.pack_rpc_gss_cred_vers_1_t(data.rpc_gss_cred_vers_1_t)
        else:
            raise XDRError, 'bad switch=%s' % data.vers

    def pack_rpc_gss_init_arg(self, data):
        if data.gss_token is None:
            raise TypeError, 'data.gss_token == None'
        self.pack_opaque(data.gss_token)

    def pack_rpc_gss_init_res(self, data):
        if data.handle is None:
            raise TypeError, 'data.handle == None'
        self.pack_opaque(data.handle)
        if data.gss_major is None:
            raise TypeError, 'data.gss_major == None'
        self.pack_uint(data.gss_major)
        if data.gss_minor is None:
            raise TypeError, 'data.gss_minor == None'
        self.pack_uint(data.gss_minor)
        if data.seq_window is None:
            raise TypeError, 'data.seq_window == None'
        self.pack_uint(data.seq_window)
        if data.gss_token is None:
            raise TypeError, 'data.gss_token == None'
        self.pack_opaque(data.gss_token)

    def pack_rpc_gss_integ_data(self, data):
        if data.databody_integ is None:
            raise TypeError, 'data.databody_integ == None'
        self.pack_opaque(data.databody_integ)
        if data.checksum is None:
            raise TypeError, 'data.checksum == None'
        self.pack_opaque(data.checksum)

    def pack_rpc_gss_data_t(self, data):
        if data.seq_num is None:
            raise TypeError, 'data.seq_num == None'
        self.pack_uint(data.seq_num)
        if data.arg is None:
            raise TypeError, 'data.arg == None'
        self.pack_proc_req_arg_t(data.arg)

    def pack_rpc_gss_priv_data(self, data):
        if data.databody_priv is None:
            raise TypeError, 'data.databody_priv == None'
        self.pack_opaque(data.databody_priv)

    def pack_gss_major_codes(self, data):
        if data not in [const.GSS_S_COMPLETE, const.GSS_S_CONTINUE_NEEDED, const.GSS_S_DUPLICATE_TOKEN, const.GSS_S_OLD_TOKEN, const.GSS_S_UNSEQ_TOKEN, const.GSS_S_GAP_TOKEN, const.GSS_S_BAD_MECH, const.GSS_S_BAD_NAME, const.GSS_S_BAD_NAMETYPE, const.GSS_S_BAD_BINDINGS, const.GSS_S_BAD_STATUS, const.GSS_S_BAD_MIC, const.GSS_S_BAD_SIG, const.GSS_S_NO_CRED, const.GSS_S_NO_CONTEXT, const.GSS_S_DEFECTIVE_TOKEN, const.GSS_S_DEFECTIVE_CREDENTIAL, const.GSS_S_CREDENTIALS_EXPIRED, const.GSS_S_CONTEXT_EXPIRED, const.GSS_S_FAILURE, const.GSS_S_BAD_QOP, const.GSS_S_UNAUTHORIZED, const.GSS_S_UNAVAILABLE, const.GSS_S_DUPLICATE_ELEMENT, const.GSS_S_NAME_NOT_MN, const.GSS_S_CALL_INACCESSIBLE_READ, const.GSS_S_CALL_INACCESSIBLE_WRITE, const.GSS_S_CALL_BAD_STRUCTURE]:
            raise XDRError, 'value=%s not in enum gss_major_codes' % data
        self.pack_int(data)

class GSSUnpacker(xdrlib.Unpacker):
    unpack_hyper = xdrlib.Unpacker.unpack_hyper
    unpack_string = xdrlib.Unpacker.unpack_string
    unpack_opaque = xdrlib.Unpacker.unpack_opaque
    unpack_int = xdrlib.Unpacker.unpack_int
    unpack_double = xdrlib.Unpacker.unpack_double
    unpack_float = xdrlib.Unpacker.unpack_float
    unpack_unsigned = xdrlib.Unpacker.unpack_uint
    unpack_quadruple = xdrlib.Unpacker.unpack_double
    unpack_uhyper = xdrlib.Unpacker.unpack_uhyper
    unpack_uint = xdrlib.Unpacker.unpack_uint
    unpack_bool = xdrlib.Unpacker.unpack_bool
    def unpack_rpc_gss_proc_t(self):
        data = self.unpack_int()
        if data not in [const.RPCSEC_GSS_DATA, const.RPCSEC_GSS_INIT, const.RPCSEC_GSS_CONTINUE_INIT, const.RPCSEC_GSS_DESTROY]:
            raise XDRError, 'value=%s not in enum rpc_gss_proc_t' % data
        return data

    def unpack_rpc_gss_service_t(self):
        data = self.unpack_int()
        if data not in [const.rpc_gss_svc_none, const.rpc_gss_svc_integrity, const.rpc_gss_svc_privacy]:
            raise XDRError, 'value=%s not in enum rpc_gss_service_t' % data
        return data

    def unpack_rpc_gss_cred_vers_1_t(self):
        data = types.rpc_gss_cred_vers_1_t()
        data.gss_proc = self.unpack_rpc_gss_proc_t()
        data.seq_num = self.unpack_uint()
        data.service = self.unpack_rpc_gss_service_t()
        data.handle = self.unpack_opaque()
        return data

    def unpack_rpc_gss_cred_t(self):
        data = types.rpc_gss_cred_t()
        data.vers = self.unpack_uint()
        if data.vers == const.RPCSEC_GSS_VERS_1:
            data.rpc_gss_cred_vers_1_t = self.unpack_rpc_gss_cred_vers_1_t()
            data.arm = data.rpc_gss_cred_vers_1_t
        else:
            raise XDRError, 'bad switch=%s' % data.vers
        return data

    def unpack_rpc_gss_init_arg(self):
        data = types.rpc_gss_init_arg()
        data.gss_token = self.unpack_opaque()
        return data

    def unpack_rpc_gss_init_res(self):
        data = types.rpc_gss_init_res()
        data.handle = self.unpack_opaque()
        data.gss_major = self.unpack_uint()
        data.gss_minor = self.unpack_uint()
        data.seq_window = self.unpack_uint()
        data.gss_token = self.unpack_opaque()
        return data

    def unpack_rpc_gss_integ_data(self):
        data = types.rpc_gss_integ_data()
        data.databody_integ = self.unpack_opaque()
        data.checksum = self.unpack_opaque()
        return data

    def unpack_rpc_gss_data_t(self):
        data = types.rpc_gss_data_t()
        data.seq_num = self.unpack_uint()
        data.arg = self.unpack_proc_req_arg_t()
        return data

    def unpack_rpc_gss_priv_data(self):
        data = types.rpc_gss_priv_data()
        data.databody_priv = self.unpack_opaque()
        return data

    def unpack_gss_major_codes(self):
        data = self.unpack_int()
        if data not in [const.GSS_S_COMPLETE, const.GSS_S_CONTINUE_NEEDED, const.GSS_S_DUPLICATE_TOKEN, const.GSS_S_OLD_TOKEN, const.GSS_S_UNSEQ_TOKEN, const.GSS_S_GAP_TOKEN, const.GSS_S_BAD_MECH, const.GSS_S_BAD_NAME, const.GSS_S_BAD_NAMETYPE, const.GSS_S_BAD_BINDINGS, const.GSS_S_BAD_STATUS, const.GSS_S_BAD_MIC, const.GSS_S_BAD_SIG, const.GSS_S_NO_CRED, const.GSS_S_NO_CONTEXT, const.GSS_S_DEFECTIVE_TOKEN, const.GSS_S_DEFECTIVE_CREDENTIAL, const.GSS_S_CREDENTIALS_EXPIRED, const.GSS_S_CONTEXT_EXPIRED, const.GSS_S_FAILURE, const.GSS_S_BAD_QOP, const.GSS_S_UNAUTHORIZED, const.GSS_S_UNAVAILABLE, const.GSS_S_DUPLICATE_ELEMENT, const.GSS_S_NAME_NOT_MN, const.GSS_S_CALL_INACCESSIBLE_READ, const.GSS_S_CALL_INACCESSIBLE_WRITE, const.GSS_S_CALL_BAD_STRUCTURE]:
            raise XDRError, 'value=%s not in enum gss_major_codes' % data
        return data

