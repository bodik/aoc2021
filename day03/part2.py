#!/usr/bin/env python3
"""
day3
"""

import logging
from argparse import ArgumentParser
from pathlib import Path

from bitarray import bitarray
from bitarray.util import ba2int


def bitcriteria(data, idx):
    """filter data items with most common value in idx bit"""

    # find most common bit value
    tmp = 0
    for line in data:
        tmp += int(line[idx])
    tmp = '1' if tmp >= len(data)/2 else '0'

    return [line for line in data if line[idx] == tmp]


def main():
    """main"""

    parser = ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()
    logging.info(args)

    data = Path(args.input).read_text('utf-8').splitlines()

    ox_data = data
    co_data = data
    for idx in range(len(data[0])):
        ox_data = bitcriteria(ox_data, idx)
        if len(ox_data) == 1:
            break

    for idx in range(len(data[0])):
        tmp = bitcriteria(co_data, idx)
        co_data = [item for item in co_data if item not in tmp]
        if len(co_data) == 1:
            break

    ox_rating = ba2int(bitarray(ox_data[0]))
    co_rating = ba2int(bitarray(co_data[0]))

    print(f'ox {ox_rating} co {co_rating} life {ox_rating*co_rating}')


if __name__ == '__main__':
    main()
