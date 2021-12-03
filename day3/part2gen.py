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


def criteria(data, idx, critfn):
    """filter data items with most common value in idx bit"""

    # count stats
    tmp = defaultdict(int)
    for line in data:
        tmp[line[idx]] += 1

    # select most common value
    # inspired by https://github.com/hyper-neutrino/advent-of-code/blob/main/2021/day3p2.py
    # where critfn over tuple also solves the item preference issue as sideeffect (min vs max vs '0' vs '1')
    # as max([(1, '0'), (1, '1')]) == (1, '1')
    tmp = critfn([(count, item) for item, count in tmp.items()])

    # filter items
    return [line for line in data if line[idx] == tmp[1]]


def main():
    """main"""

    parser = ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()
    logging.info(args)

    data = Path(args.input).read_text('utf-8').splitlines()

    ox_data = data
    for idx in range(len(data[0])):
        ox_data = criteria(ox_data, idx, max)
        if len(ox_data) == 1:
            break

    co_data = data
    for idx in range(len(data[0])):
        co_data = criteria(co_data, idx, min)
        if len(co_data) == 1:
            break

    ox_rating = ba2int(bitarray(ox_data[0]))
    co_rating = ba2int(bitarray(co_data[0]))

    print(f'ox {ox_rating} co {co_rating} life {ox_rating*co_rating}')


if __name__ == '__main__':
    main()
