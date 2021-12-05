#!/usr/bin/env python3
"""
aoc2021 solution skeleton
"""

import logging
from argparse import ArgumentParser
from collections import defaultdict
from pathlib import Path

from bresenham import bresenham


def is_horizontal(start, end):
    """x is horizonal"""

    return start[0] == end[0]


def is_vertical(start, end):
    """y is horizonal"""

    return start[1] == end[1]


def is_diagonal(start, end):
    """x and y distance should be equal"""

    return (abs(start[0] - end[0]) == abs(start[1] - end[1]))


def main():
    """main"""

    parser = ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()
    logging.info(args)

    data = Path(args.input).read_text('utf-8').splitlines()

    vents = defaultdict(int)
    for start, _, end in map(str.split, data):
        start = tuple(map(int, start.split(',')))
        end = tuple(map(int, end.split(',')))

        if not (
            is_horizontal(start, end)
            or is_vertical(start, end)
            or is_diagonal(start, end)
        ):
            continue

        for point in bresenham(*start, *end):
            vents[point] += 1

    overlaps = list(filter(lambda x: x[1] >= 2, vents.items()))
    print(f'overlaps {len(overlaps)}')


if __name__ == '__main__':
    main()
