# -*- coding: utf-8 -*-

"""
A module providing functions, classes to be included in the package.
"""


from cobs.cobs import decode
import struct
import numpy as np
import json
from .utils import export


class Frame():

    def __init__(self, log_id, timestamp, samplecount, payload):
        self.log_id = log_id
        self.timestamp = timestamp
        self.samplecount = samplecount
        self.payload = payload
        self._data_type = None

    @property
    def data_type(self):
        return self._data_type

    @data_type.setter
    def data_type(self, data_type):
        self._data_type = np.dtype(data_type.lower())
        self._data_type.newbyteorder('<')

    def set_data_type(self, data_type):
        self.data_type = data_type
        return self

    @property
    def data(self):
        return np.frombuffer(self.payload, dtype=self._data_type)

    def as_dict(self):
        dct = {'log_id': self.log_id,
               'timestamp': self.timestamp,
               'samplecount': self.samplecount,
               'payload': self.payload}

        return dct

    def as_json(self):
        dct = self.as_dict()
        dct['payload'] = dct['payload'].hex()

        return json.dumps(dct)

    def __repr__(self):
        dct = {'log_id': self.log_id,
               'timestamp': self.timestamp,
               'samplecount': self.samplecount,
               'payload': self.payload.hex()}
        return repr(dct)


@export
def decobs(cobsed):
    """Decode COBS-encoded data stream."""
    return [decode(packet) for packet in cobsed.split(b'\x00')]


@export
def unpack(msgs):
    """
    Parse list of raw packets.

    Outputs frame-form with log-ID, timestamp, sample count, and payload.
    """
    return [Frame(*struct.unpack('<HHH%ds' % (len(msg) - 6), msg))
            if len(msg) > 0
            else Frame(None, None, None, b'') for msg in msgs]


@export
def apply_types(frames, type_dict):
    return [f.set_data_type(type_dict[f.log_id]) if f.log_id in type_dict
            else f for f in frames]
