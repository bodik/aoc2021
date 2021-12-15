#!/usr/bin/env python3
"""
aoc2021 solution skeleton
"""

import logging
import operator
from argparse import ArgumentParser
from pathlib import Path

import numpy as np
from dijkstar import Graph, find_path


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


def main():
    """main"""

    parser = ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()
    logging.info(args)

    data = Path(args.input).read_text('utf-8').splitlines()
    data = np.array(list(map(list, data)), dtype=int)
    rows, cols = data.shape
    print(data)

    graph = Graph()
    for row in range(rows):
        for col in range(cols):
            point_id = row * cols + col
            for point in get_adjacent_points((row, col), data.shape):
                point1_id = point[0] * cols + point[1]
                graph.add_edge(point_id, point1_id, data[point])

    print(find_path(graph, 0, rows*cols-1))


if __name__ == '__main__':
    main()
