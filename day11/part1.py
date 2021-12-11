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
    parser.add_argument('steps', type=int)
    args = parser.parse_args()
    logging.info(args)

    data = Path(args.input).read_text('utf-8').splitlines()
    data = np.array(list(map(list, data)), dtype=int)
    rows, cols = data.shape

    total = 0
    print('init')
    print(data)

    for step in range(args.steps):
        queue = []
        flashed = []

        for row in range(rows):
            for col in range(cols):
                octo = (row, col)
                data[octo] += 1
                if data[octo] > 9:
                    queue.append(octo)

        while queue:
            octo = queue.pop()
            if octo in flashed:
                continue

            for adj in get_adjacent_points(octo, data.shape):
                data[adj] += 1
                if data[adj] > 9:
                    queue.append(adj)

            flashed.append(octo)

        for octo in flashed:
            data[octo] = 0
            total += 1

        #print(f'after step {step+1}')
        #print(data)

    print(f'total {total}')


if __name__ == '__main__':
    main()
