#!/usr/bin/env python3
"""
somewhat modified algorithm inspired by @happyCerberus
it's wierd 
"""

import logging
import operator
from argparse import ArgumentParser
from pathlib import Path

import numpy as np


def get_adjacent_points(point, boundary):
    points = []

    for vector in [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]:
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

    step = 0
    while True:
        step += 1

        queue = set()
        flashes = 0

        for row in range(rows):
            for col in range(cols):
                octo = (row, col)
                data[octo] += 1
                if data[octo] > 9:
                    queue.add(octo)

        while queue:
            octo = queue.pop()

            data[octo] = 0
            flashes += 1

            for adj in get_adjacent_points(octo, data.shape):
                if data[adj] != 0:
                    data[adj] += 1
                if data[adj] > 9:
                    queue.add(adj)

        if flashes == (rows * cols):
            break

    print(f'step {step}')


if __name__ == '__main__':
    main()
