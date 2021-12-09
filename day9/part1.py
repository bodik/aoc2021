#!/usr/bin/env python3
"""
aoc2021 solution skeleton
"""

import logging
import operator
from argparse import ArgumentParser
from pathlib import Path

import numpy as np


def get_adjacent_points(point, boundary):
    points = []

    for vector in [(-1,0), (0, 1), (1, 0), (0, -1)]:
        tmp = tuple(map(operator.add, point, vector))
        if (tmp[0] < 0) or (tmp[0] > boundary[0]-1):
            continue
        if (tmp[1] < 0) or (tmp[1] > boundary[1]-1):
            continue
        points.append(tmp)

    return points


def main():
    """main"""

    parser = ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()
    logging.info(args)

    data = Path(args.input).read_text('utf-8').splitlines()
    data = np.array(list(map(list, data)), dtype=int)
    rows, cols = data.shape

    risk = 0

    for r in range(rows):
        for c in range(cols):
            adjacent = get_adjacent_points((r,c), data.shape)
            values = [data[x] for x in adjacent]
            if all(data[r,c] < x for x in values):
                risk += data[r,c]+1

    print(f'risk {risk}')


if __name__ == '__main__':
    main()
