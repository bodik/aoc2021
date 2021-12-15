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


COEF = 5


def parse_input(inputfile):
    data = Path(inputfile).read_text('utf-8').splitlines()
    data = np.array(list(map(list, data)), dtype=int)
    rows, cols = data.shape
    print(data)

    matrix = np.full((rows*COEF, cols*COEF), 0)
    for itrow in range(COEF):
        for itcol in range(COEF):
            for row in range(rows):
                for col in range(cols):
                    xrow = (rows*itrow) + row
                    xcol = (cols*itcol) + col
                    matrix[xrow, xcol] = data[row, col] + itrow + itcol
                    if matrix[xrow, xcol] > 9:
                        matrix[xrow, xcol] = matrix[xrow, xcol] % 9
    print(matrix)

    return matrix


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

    matrix = parse_input(args.input)
    rows, cols = matrix.shape

    graph = Graph()
    for row in range(rows):
        for col in range(cols):
            point_id = row * cols + col
            for point in get_adjacent_points((row, col), matrix.shape):
                point1_id = point[0] * cols + point[1]
                graph.add_edge(point_id, point1_id, matrix[point])

    print(find_path(graph, 0, rows*cols-1))


if __name__ == '__main__':
    main()
