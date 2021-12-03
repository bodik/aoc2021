#!/usr/bin/env python3
"""
day3
"""

import logging
from argparse import ArgumentParser
from pathlib import Path

from bitarray import bitarray
from bitarray.util import ba2int


def main():
    """main"""

    parser = ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()
    logging.info(args)

    data = Path(args.input).read_text('utf-8').splitlines()
    data_len = len(data)
    tmp = [0] * len(data[0])

    for line in data:
        for idx in range(len(line)):
            tmp[idx] += int(line[idx])

    tmp = bitarray((1 if bit > data_len/2 else 0) for bit in tmp)
    gamma = ba2int(tmp)
    epsilon = ba2int(~tmp)

    print(f'gamma {gamma} epsilon {epsilon} power {gamma*epsilon}')


if __name__ == '__main__':
    main()
