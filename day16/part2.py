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


class Header:
    def __init__(self, bits):
        self.version = ba2int(bits[:3])
        self.type_id = ba2int(bits[3:6])
        self.hlen = 6


class Literal(Header):
    def __init__(self, bits):
        super().__init__(bits)
        self._value = ''

        ptr = 0
        while True:
            tmp = bits[self.hlen+ptr: self.hlen+ptr+5]
            self._value += tmp[1:].to01()
            ptr += 5
            if tmp[0] == 0:
                break

        self._value = ba2int(bitarray(self._value)) if self._value else None
        self.len = self.hlen + ptr

    def value(self):
        return self._value


class Operator(Header):
    def __init__(self, bits):
        super().__init__(bits)
        self.length_type_id = bits[self.hlen]
        self.packets = []

        if self.length_type_id == 0:  # total len
            self.len = self.hlen+1+15
            total = ba2int(bits[self.hlen+1: self.hlen+1+15])
            consumed = 0
            while consumed < total:
                packet = packet_factory(bits[self.hlen+1+15+consumed:])
                consumed += packet.len
                self.packets.append(packet)
            self.len += consumed
        elif self.length_type_id == 1:  # number of packets
            self.len = self.hlen+1+11
            number_of_packets = ba2int(bits[self.hlen+1: self.hlen+1+11])
            consumed = 0
            for _ in range(number_of_packets):
                packet = packet_factory(bits[self.hlen+1+11+consumed:])
                consumed += packet.len
                self.packets.append(packet)
            self.len += consumed
        else:
            raise ValueError('ivalid operator length_type_id')

    def value(self):
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


def packet_factory(bits):
    """packet factory"""

    header = Header(bits)
    if header.type_id == 4:  # Literal
        packet = Literal(bits)
    else:
        packet = Operator(bits)
    return packet


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
    packet = packet_factory(hex2ba('D2FE28'))
    assert packet.value() == 2021
    packet = packet_factory(hex2ba('38006F45291200'))
    assert len(packet.packets) == 2
    packet = packet_factory(hex2ba('EE00D40C823060'))
    assert len(packet.packets) == 3
    assert sum_versions(packet_factory(hex2ba('8A004A801A8002F478'))) == 16
    assert sum_versions(packet_factory(hex2ba('620080001611562C8802118E34'))) == 12
    assert sum_versions(packet_factory(hex2ba('C0015000016115A2E0802F182340'))) == 23
    assert sum_versions(packet_factory(hex2ba('A0016C880162017C3686B18A3D4780'))) == 31

    # tests part2
    assert packet_factory(hex2ba('C200B40A82')).value() == 3
    assert packet_factory(hex2ba('04005AC33890')).value() == 54
    assert packet_factory(hex2ba('880086C3E88112')).value() == 7
    assert packet_factory(hex2ba('CE00C43D881120')).value() == 9
    assert packet_factory(hex2ba('D8005AC2A8F0')).value() == 1
    assert packet_factory(hex2ba('F600BC2D8F')).value() == 0
    assert packet_factory(hex2ba('9C0141080250320F1802104A08')).value() == 1

    # run
    data = Path(args.input).read_text('utf-8').strip()
    result = packet_factory(hex2ba(data)).value()
    print(f'result {result}')


if __name__ == '__main__':
    main()
