# -*- coding: utf-8 -*-

"""
A module providing functions, classes to be included in the package.
"""


from cobs.cobs import decode
from struct import unpack
from .utils import export


@export
def decodePacket(pkt):
    raw = pkt.read(pkt.inWaiting())
    packet = raw.split('\x00')[0]
    packet = decode(packet)
    packet = unpack('<HH%ds' % (len(packet)-4), packet)
    return packet
