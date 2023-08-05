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
from cfxdb.gen.xbr import Actor as ActorGen
from zlmdb import table, MapUuidBytes20Uint8FlatBuffers


class _ActorGen(ActorGen.Actor):
    """
    Expand methods on the class code generated by flatc.

    FIXME: come up with a PR for flatc to generated this stuff automatically.
    """
    @classmethod
    def GetRootAsActor(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = _ActorGen()
        x.Init(buf, n + offset)
        return x

    def ActorAsBytes(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            _off = self._tab.Vector(o)
            _len = self._tab.VectorLen(o)
            return memoryview(self._tab.Bytes)[_off:_off + _len]
        return None

    def MarketAsBytes(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            _off = self._tab.Vector(o)
            _len = self._tab.VectorLen(o)
            return memoryview(self._tab.Bytes)[_off:_off + _len]
        return None

    def JoinedAsBytes(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(12))
        if o != 0:
            _off = self._tab.Vector(o)
            _len = self._tab.VectorLen(o)
            return memoryview(self._tab.Bytes)[_off:_off + _len]
        return None

    def SecurityAsBytes(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(14))
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


class Actor(object):
    """
    XBR Market Actors.
    """
    def __init__(self, from_fbs=None):
        self._from_fbs = from_fbs

        # [uint8] (address)
        self._actor = None

        # uint8 (ActorType)
        self._actor_type = None

        # [uint8] (uuid)
        self._market = None

        # uint64 (timestamp)
        self._timestamp = None

        # [uint8] (uint256)
        self._joined = None

        # [uint8] (uint256)
        self._security = None

        # string (multihash)
        self._meta = None

        # [uint8] (ethhash)
        self._tid = None

        # [uint8] (ethsig)
        self._signature = None

    def marshal(self) -> dict:
        obj = {
            'timestamp': int(self.timestamp) if self.timestamp else None,
            'market': self.market.bytes if self.market else None,
            'actor': bytes(self.actor) if self.actor else None,
            'actor_type': self.actor_type,
            'joined': pack_uint256(self.joined) if self.joined else None,
            'security': pack_uint256(self.security) if self.security else None,
            'meta': self.meta,
            'tid': bytes(self.tid) if self.tid else None,
            'signature': bytes(self.signature) if self.signature else None,
        }
        return obj

    def __str__(self):
        return '\n{}\n'.format(pprint.pformat(self.marshal()))

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
    def market(self) -> uuid.UUID:
        """
        ID of the market this actor is associated with.
        """
        if self._market is None and self._from_fbs:
            if self._from_fbs.MarketLength():
                _market = self._from_fbs.MarketAsBytes()
                self._market = uuid.UUID(bytes=bytes(_market))
        return self._market

    @market.setter
    def market(self, value: uuid.UUID):
        assert value is None or isinstance(value, uuid.UUID)
        self._market = value

    @property
    def actor(self) -> bytes:
        """
        Ethereum address of the member.
        """
        if self._actor is None and self._from_fbs:
            if self._from_fbs.ActorLength():
                self._actor = self._from_fbs.ActorAsBytes()
        return self._actor

    @actor.setter
    def actor(self, value: bytes):
        assert value is None or (type(value) == bytes and len(value) == 20)
        self._actor = value

    @property
    def actor_type(self) -> int:
        """
        Type of the market actor.
        """
        if self._actor_type is None and self._from_fbs:
            self._actor_type = self._from_fbs.ActorType()
        return self._actor_type

    @actor_type.setter
    def actor_type(self, value: int):
        assert value is None or type(value) == int
        self._actor_type = value

    @property
    def joined(self) -> int:
        """
        Block number (on the blockchain) when the actor (originally) joined the market.
        """
        if self._joined is None and self._from_fbs:
            if self._from_fbs.JoinedLength():
                _joined = self._from_fbs.JoinedAsBytes()
                self._joined = unpack_uint256(bytes(_joined))
            else:
                self._joined = 0
        return self._joined

    @joined.setter
    def joined(self, value: int):
        assert value is None or type(value) == int
        self._joined = value

    @property
    def security(self) -> int:
        """
        Security (XBR tokens) deposited by the actor in the market.
        """
        if self._security is None and self._from_fbs:
            if self._from_fbs.SecurityLength():
                security = self._from_fbs.SecurityAsBytes()
                self._security = unpack_uint256(bytes(security))
            else:
                self._security = 0
        return self._security

    @security.setter
    def security(self, value: int):
        assert value is None or type(value) == int, 'security must be int, was: {}'.format(value)
        self._security = value

    @property
    def meta(self) -> str:
        """
        The XBR market metadata published by the market owner. IPFS Multihash pointing to a RDF/Turtle file with market metadata.
        """
        if self._meta is None and self._from_fbs:
            meta = self._from_fbs.Meta()
            if meta:
                self._meta = meta.decode('utf8')
        return self._meta

    @meta.setter
    def meta(self, value: str):
        assert value is None or type(value) == str
        self._meta = value

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
        When signed off-chain and submitted via ``XBRMarket.joinMarketFor``.
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
        return Actor(_ActorGen.GetRootAsActor(buf, 0))

    def build(self, builder):

        market = self.market.bytes if self.market else None
        if market:
            market = builder.CreateString(market)

        actor = self.actor
        if actor:
            actor = builder.CreateString(actor)

        joined = self.joined
        if joined:
            joined = builder.CreateString(pack_uint256(joined))

        security = self.security
        if security:
            security = builder.CreateString(pack_uint256(security))

        meta = self.meta
        if meta:
            meta = builder.CreateString(meta)

        tid = self.tid
        if tid:
            tid = builder.CreateString(tid)

        signature = self.signature
        if signature:
            signature = builder.CreateString(signature)

        ActorGen.ActorStart(builder)

        if self.timestamp:
            ActorGen.ActorAddTimestamp(builder, int(self.timestamp))

        if market:
            ActorGen.ActorAddMarket(builder, market)

        if actor:
            ActorGen.ActorAddActor(builder, actor)

        if self.actor_type:
            ActorGen.ActorAddActorType(builder, self.actor_type)

        if joined:
            ActorGen.ActorAddJoined(builder, joined)

        if security:
            ActorGen.ActorAddSecurity(builder, security)

        if meta:
            ActorGen.ActorAddMeta(builder, meta)

        if tid:
            ActorGen.ActorAddTid(builder, tid)

        if signature:
            ActorGen.ActorAddSignature(builder, signature)

        final = ActorGen.ActorEnd(builder)

        return final


@table('1863eb64-322a-42dd-9fce-a59c99d5b40e', build=Actor.build, cast=Actor.cast)
class Actors(MapUuidBytes20Uint8FlatBuffers):
    """
    Market actors table, mapping from ``(market_id|UUID, actor_adr|bytes[20], actor_type|int)`` to :class:`cfxdb.xbr.Actor`.
    """
