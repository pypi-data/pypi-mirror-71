##############################################################################
#
#                        Crossbar.io FX
#     Copyright (C) Crossbar.io Technologies GmbH. All rights reserved.
#
##############################################################################

import pprint
import uuid

import flatbuffers
import numpy as np
from cfxdb import unpack_uint256, pack_uint256
from cfxdb.gen.xbr import Member as MemberGen
from cfxdb.gen.xbr.MemberLevel import MemberLevel
from zlmdb import table, MapBytes20FlatBuffers


class _MemberGen(MemberGen.Member):
    """
    Expand methods on the class code generated by flatc.

    FIXME: come up with a PR for flatc to generated this stuff automatically.
    """
    @classmethod
    def GetRootAsMember(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = _MemberGen()
        x.Init(buf, n + offset)
        return x

    def AddressAsBytes(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            _off = self._tab.Vector(o)
            _len = self._tab.VectorLen(o)
            return memoryview(self._tab.Bytes)[_off:_off + _len]
        return None

    def AccountOidAsBytes(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            _off = self._tab.Vector(o)
            _len = self._tab.VectorLen(o)
            return memoryview(self._tab.Bytes)[_off:_off + _len]
        return None

    def RegisteredAsBytes(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(10))
        if o != 0:
            _off = self._tab.Vector(o)
            _len = self._tab.VectorLen(o)
            return memoryview(self._tab.Bytes)[_off:_off + _len]
        return None

    def TidAsBytes(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(18))
        if o != 0:
            _off = self._tab.Vector(o)
            _len = self._tab.VectorLen(o)
            return memoryview(self._tab.Bytes)[_off:_off + _len]
        return None

    def SignatureAsBytes(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(20))
        if o != 0:
            _off = self._tab.Vector(o)
            _len = self._tab.VectorLen(o)
            return memoryview(self._tab.Bytes)[_off:_off + _len]
        return None


class Member(object):
    """
    XBR Network member database object.
    """
    def __init__(self, from_fbs=None):
        self._from_fbs = from_fbs

        # [uint8] (address)
        self._address = None

        # [uint8] (uuid)
        self._account_oid = None

        # uint64 (timestamp)
        self._timestamp = None

        # [uint8] (uint256)
        self._registered = None

        # string (multihash)
        self._eula = None

        # string (multihash)
        self._profile = None

        # enum MemberLevel: uint8
        self._level = None

        # [uint8] (ethhash)
        self._tid = None

        # [uint8] (ethsig)
        self._signature = None

    def marshal(self) -> dict:
        obj = {
            'address': self.address,
            'account_oid': self._account_oid.bytes if self._account_oid else None,
            'timestamp': self.timestamp,
            'registered': self.registered,
            'eula': self.eula,
            'profile': self.profile,
            'level': self.level,
            'tid': bytes(self.tid) if self.tid else None,
            'signature': bytes(self.signature) if self.signature else None,
        }
        return obj

    def __str__(self):
        return '\n{}\n'.format(pprint.pformat(self.marshal()))

    @property
    def address(self) -> bytes:
        """
        Ethereum address of the member.
        """
        if self._address is None and self._from_fbs:
            if self._from_fbs.AddressLength():
                self._address = self._from_fbs.AddressAsBytes()
        return self._address

    @address.setter
    def address(self, value: bytes):
        assert value is None or (type(value) == bytes and len(value) == 20)
        self._address = value

    @property
    def account_oid(self) -> uuid.UUID:
        """
        ID of user account this member has an account on planet.xbr.network.
        """
        if self._account_oid is None and self._from_fbs:
            if self._from_fbs.AccountOidLength():
                _account_oid = self._from_fbs.AccountOidAsBytes()
                self._account_oid = uuid.UUID(bytes=bytes(_account_oid))
            else:
                self._account_oid = uuid.UUID(bytes=b'\x00' * 16)
        return self._account_oid

    @account_oid.setter
    def account_oid(self, value: uuid.UUID):
        assert value is None or isinstance(value, uuid.UUID)
        self._account_oid = value

    @property
    def timestamp(self) -> np.datetime64:
        """
        Database transaction time (epoch time in ns) of insert or last update.
        """
        if self._timestamp is None and self._from_fbs:
            self._timestamp = np.datetime64(self._from_fbs.Timestamp(), 'ns')
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value: np.datetime64):
        assert value is None or isinstance(value, np.datetime64)
        self._timestamp = value

    @property
    def registered(self) -> int:
        """
        Block number (on the blockchain) when the member (originally) registered.
        """
        if self._registered is None and self._from_fbs:
            if self._from_fbs.RegisteredLength():
                _registered = self._from_fbs.RegisteredAsBytes()
                self._registered = unpack_uint256(bytes(_registered))
            else:
                self._registered = 0
        return self._registered

    @registered.setter
    def registered(self, value: int):
        assert value is None or type(value) == int
        self._registered = value

    @property
    def eula(self) -> str:
        """
        EULA the member agreed to when joining the market (IPFS Multihash string).
        """
        if self._eula is None and self._from_fbs:
            eula = self._from_fbs.Eula()
            if eula:
                self._eula = eula.decode('utf8')
        return self._eula

    @eula.setter
    def eula(self, value):
        assert value is None or type(value) == str
        self._eula = value

    @property
    def profile(self) -> str:
        """
        Optional member profile (IPFS Multihash string).
        """
        if self._profile is None and self._from_fbs:
            profile = self._from_fbs.Profile()
            if profile:
                self._profile = profile.decode('utf8')
        return self._profile

    @profile.setter
    def profile(self, value):
        assert value is None or type(value) == str
        self._profile = value

    @property
    def level(self) -> int:
        """
        Current member level.
        """
        if self._level is None and self._from_fbs:
            self._level = self._from_fbs.Level()
        return self._level

    @level.setter
    def level(self, value: int):
        assert value is None or type(value) == int
        assert value in [
            MemberLevel.NONE, MemberLevel.ACTIVE, MemberLevel.VERIFIED, MemberLevel.RETIRED,
            MemberLevel.PENALTY, MemberLevel.BLOCKED
        ]
        self._level = value

    @property
    def tid(self) -> bytes:
        """
        Transaction hash of the transaction this change was committed to the blockchain under.
        """
        if self._tid is None and self._from_fbs:
            if self._from_fbs.TidLength():
                self._tid = self._from_fbs.TidAsBytes()
        return self._tid

    @tid.setter
    def tid(self, value: bytes):
        assert value is None or (type(value) == bytes and len(value) == 32)
        self._tid = value

    @property
    def signature(self) -> bytes:
        """
        When signed off-chain and submitted via ``XBRNetwork.registerMemberFor``.
        """
        if self._signature is None and self._from_fbs:
            if self._from_fbs.SignatureLength():
                self._signature = self._from_fbs.SignatureAsBytes()
        return self._signature

    @signature.setter
    def signature(self, value: bytes):
        assert value is None or (type(value) == bytes and len(value) == 65)
        self._signature = value

    @staticmethod
    def cast(buf):
        return Member(_MemberGen.GetRootAsMember(buf, 0))

    def build(self, builder):

        address = self.address
        if address:
            address = builder.CreateString(address)

        account_oid = self.account_oid
        if account_oid:
            account_oid = builder.CreateString(account_oid.bytes)

        registered = self.registered
        if registered:
            registered = builder.CreateString(pack_uint256(registered))

        eula = self.eula
        if eula:
            eula = builder.CreateString(eula)

        profile = self.profile
        if profile:
            profile = builder.CreateString(profile)

        tid = self.tid
        if tid:
            tid = builder.CreateString(tid)

        signature = self.signature
        if signature:
            signature = builder.CreateString(signature)

        MemberGen.MemberStart(builder)

        if address:
            MemberGen.MemberAddAddress(builder, address)

        if account_oid:
            MemberGen.MemberAddAccountOid(builder, account_oid)

        if self.timestamp:
            MemberGen.MemberAddTimestamp(builder, int(self.timestamp))

        if registered:
            MemberGen.MemberAddRegistered(builder, registered)

        if eula:
            MemberGen.MemberAddEula(builder, eula)

        if profile:
            MemberGen.MemberAddProfile(builder, profile)

        if self.level:
            MemberGen.MemberAddLevel(builder, self.level)

        if tid:
            MemberGen.MemberAddTid(builder, tid)

        if signature:
            MemberGen.MemberAddSignature(builder, signature)

        final = MemberGen.MemberEnd(builder)

        return final


@table('d1808139-5a3b-4a4e-abad-152dd4cd1131', build=Member.build, cast=Member.cast)
class Members(MapBytes20FlatBuffers):
    """
    XBR members by ``member_adr``.

    Map :class:`zlmdb.MapBytes20FlatBuffers` from ``member_adr`` to :class:`cfxdb.xbr.Member`
    """
