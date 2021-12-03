#!/usr/bin/env python3
"""
we might expect some more variations on the theme, so
lets prepare for sprint
"""

import logging
from argparse import ArgumentParser
from collections import defaultdict
from pathlib import Path

from bitarray import bitarray
from bitarray.util import ba2int


def criteria(data, idx):
    """filter data items with most common value in idx bit"""

    # find most common value
    tmp = defaultdict(int)
    for line in data:
        tmp[line[idx]] += 1

    # sort by key names to honor '1' in ties, required py37+
    tmp = {k: v for k, v in sorted(tmp.items(), key=lambda item: item[0], reverse=True)}

    # select most common value
    tmp = max(tmp, key=tmp.get)

    # filter items
    return [line for line in data if line[idx] == tmp]


def main():
    """main"""

    parser = ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()
    logging.info(args)

    data = Path(args.input).read_text('utf-8').splitlines()

    ox_data = data
    for idx in range(len(data[0])):
        ox_data = criteria(ox_data, idx)
        if len(ox_data) == 1:
            break

    co_data = data
    for idx in range(len(data[0])):
        tmp = criteria(co_data, idx)
        co_data = [item for item in co_data if item not in tmp]
        if len(co_data) == 1:
            break

    ox_rating = ba2int(bitarray(ox_data[0]))
    co_rating = ba2int(bitarray(co_data[0]))

    print(f'ox {ox_rating} co {co_rating} life {ox_rating*co_rating}')


if __name__ == '__main__':
    main()
