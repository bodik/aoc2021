#!/usr/bin/env python3
"""
aoc2021 solution skeleton
"""

import logging
from argparse import ArgumentParser
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
        self.value = ''

        ptr = 0
        while True:
            tmp = bits[self.hlen+ptr: self.hlen+ptr+5]
            self.value += tmp[1:].to01()
            ptr += 5
            if tmp[0] == 0:
                break

        self.value = ba2int(bitarray(self.value)) if self.value else None
        self.len = self.hlen + ptr


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
                packet = parse_packet(bits[self.hlen+1+15+consumed:])
                consumed += packet.len
                self.packets.append(packet)
            self.len += consumed
        elif self.length_type_id == 1:  # number of packets
            self.len = self.hlen+1+11
            number_of_packets = ba2int(bits[self.hlen+1: self.hlen+1+11])
            consumed = 0
            for _ in range(number_of_packets):
                packet = parse_packet(bits[self.hlen+1+11+consumed:])
                consumed += packet.len
                self.packets.append(packet)
            self.len += consumed
        else:
            raise ValueError('ivalid operator length_type_id')


def parse_packet(bits):
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

    # tests
    packet = parse_packet(hex2ba('D2FE28'))
    assert packet.value == 2021
    packet = parse_packet(hex2ba('38006F45291200'))
    assert len(packet.packets) == 2
    packet = parse_packet(hex2ba('EE00D40C823060'))
    assert len(packet.packets) == 3
    assert sum_versions(parse_packet(hex2ba('8A004A801A8002F478'))) == 16
    assert sum_versions(parse_packet(hex2ba('620080001611562C8802118E34'))) == 12
    assert sum_versions(parse_packet(hex2ba('C0015000016115A2E0802F182340'))) == 23
    assert sum_versions(parse_packet(hex2ba('A0016C880162017C3686B18A3D4780'))) == 31

    # run
    data = Path(args.input).read_text('utf-8').strip()
    result = sum_versions(parse_packet(hex2ba(data)))
    print(f'result {result}')


if __name__ == '__main__':
    main()
