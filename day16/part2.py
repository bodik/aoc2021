#!/usr/bin/env python3
"""
aoc2021 solution skeleton
"""

import logging
from argparse import ArgumentParser
from math import prod
from pathlib import Path

from bitarray import bitarray
from bitarray.util import ba2int, hex2ba


class Packet:  # pylint: disable=too-few-public-methods
    def __init__(self, bits):
        self.version = ba2int(bits[:3])
        self.type_id = ba2int(bits[3:6])
        self.hlen = 6

    @staticmethod
    def factory(bits):
        """packet factory"""

        type_id = ba2int(bits[3:6])

        if type_id == 4:
            return Literal(bits)

        return Operator(bits)


class Literal(Packet):
    def __init__(self, bits):
        super().__init__(bits)
        self._value = bitarray()
        ptr = 0
        while True:
            tmp = bits[self.hlen+ptr: self.hlen+ptr+5]
            self._value += tmp[1:]
            ptr += 5
            if tmp[0] == 0:
                break
        self._value = ba2int(self._value)
        self.len = self.hlen + ptr

    def value(self):
        return self._value


class Operator(Packet):
    FLEN_TYPEID = 1
    FLEN_TOTAL = 15
    FLEN_COUNTER = 11

    def __init__(self, bits):
        super().__init__(bits)
        self.length_type_id = bits[self.hlen]
        self.packets = []

        # content specified via total length
        if self.length_type_id == 0:
            total = ba2int(bits[self.hlen+self.FLEN_TYPEID:self.hlen+self.FLEN_TYPEID+self.FLEN_TOTAL])
            self.len = self.hlen + self.FLEN_TYPEID + self.FLEN_TOTAL + total
            consumed = 0
            while consumed < total:
                packet = Packet.factory(bits[self.hlen+self.FLEN_TYPEID+self.FLEN_TOTAL+consumed:])
                consumed += packet.len
                self.packets.append(packet)

        # content specified via number of packets
        elif self.length_type_id == 1:
            counter = ba2int(bits[self.hlen+self.FLEN_TYPEID: self.hlen+self.FLEN_TYPEID+self.FLEN_COUNTER])
            consumed = 0
            for _ in range(counter):
                packet = Packet.factory(bits[self.hlen+self.FLEN_TYPEID+self.FLEN_COUNTER+consumed:])
                consumed += packet.len
                self.packets.append(packet)
            self.len = self.hlen + self.FLEN_TYPEID + self.FLEN_COUNTER + consumed

        # content type invalid
        else:
            raise ValueError('ivalid operator length_type_id')

    def value(self):  # pylint: disable=too-many-return-statements
        if self.type_id == 0:  # sum
            return sum(x.value() for x in self.packets)
        if self.type_id == 1:  # product
            return prod([x.value() for x in self.packets])
        if self.type_id == 2:  # min
            return min([x.value() for x in self.packets])
        if self.type_id == 3:  # max
            return max([x.value() for x in self.packets])
        if self.type_id == 5:  # gt
            return int(self.packets[0].value() > self.packets[1].value())
        if self.type_id == 6:  # lt
            return int(self.packets[0].value() < self.packets[1].value())
        if self.type_id == 7:  # eq
            return int(self.packets[0].value() == self.packets[1].value())
        raise ValueError('invalid operator type_id')


def sum_versions(packet):
    queue = [packet]
    accumulator = 0
    while queue:
        current = queue.pop(0)
        accumulator += current.version
        if hasattr(current, 'packets'):
            queue += current.packets

    return accumulator


def main():
    """main"""

    parser = ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()
    logging.info(args)

    # tests part1
    assert Packet.factory(hex2ba('D2FE28')).value() == 2021
    assert len(Packet.factory(hex2ba('38006F45291200')).packets) == 2
    assert len(Packet.factory(hex2ba('EE00D40C823060')).packets) == 3
    assert sum_versions(Packet.factory(hex2ba('8A004A801A8002F478'))) == 16
    assert sum_versions(Packet.factory(hex2ba('620080001611562C8802118E34'))) == 12
    assert sum_versions(Packet.factory(hex2ba('C0015000016115A2E0802F182340'))) == 23
    assert sum_versions(Packet.factory(hex2ba('A0016C880162017C3686B18A3D4780'))) == 31

    # tests part2
    assert Packet.factory(hex2ba('C200B40A82')).value() == 3
    assert Packet.factory(hex2ba('04005AC33890')).value() == 54
    assert Packet.factory(hex2ba('880086C3E88112')).value() == 7
    assert Packet.factory(hex2ba('CE00C43D881120')).value() == 9
    assert Packet.factory(hex2ba('D8005AC2A8F0')).value() == 1
    assert Packet.factory(hex2ba('F600BC2D8F')).value() == 0
    assert Packet.factory(hex2ba('9C0141080250320F1802104A08')).value() == 1

    # run
    data = Path(args.input).read_text('utf-8').strip()
    result = Packet.factory(hex2ba(data)).value()
    print(f'result {result}')


if __name__ == '__main__':
    main()
