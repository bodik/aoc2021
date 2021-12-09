#!/usr/bin/env python3
"""
aoc2021 solution skeleton
"""

import logging
import operator
from argparse import ArgumentParser
from functools import reduce
from pathlib import Path

import numpy as np


def get_adjacent_points(point, boundary):
    points = []

    for vector in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
        tmp = tuple(map(operator.add, point, vector))
        if (tmp[0] < 0) or (tmp[0] > boundary[0]-1):
            continue
        if (tmp[1] < 0) or (tmp[1] > boundary[1]-1):
            continue
        points.append(tmp)

    return points


def get_sinks(data):
    sinks = []
    rows, cols = data.shape

    for row in range(rows):
        for col in range(cols):
            adjacent = get_adjacent_points((row, col), data.shape)
            values = [data[x] for x in adjacent]
            if all(data[row, col] < x for x in values):
                sinks.append((row, col))

    return sinks


def get_basin(data, sink):
    basin = [sink]

    search = [sink]
    while search:
        cur = search.pop()
        for adj in get_adjacent_points(cur, data.shape):
            if (adj not in basin) and (data[adj] != 9) and (data[adj] > data[cur]):
                search.append(adj)
                basin.append(adj)

    return basin


def main():
    """main"""

    parser = ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()
    logging.info(args)

    data = Path(args.input).read_text('utf-8').splitlines()
    data = np.array(list(map(list, data)), dtype=int)

    sinks = get_sinks(data)
    basins = [get_basin(data, sink) for sink in sinks]

    basin_sizes = [len(x) for x in basins]
    result = reduce(lambda a, b: a*b, sorted(basin_sizes, reverse=True)[:3])
    print(f'result {result}')


if __name__ == '__main__':
    main()
