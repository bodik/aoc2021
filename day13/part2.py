#!/usr/bin/env python3
"""
aoc2021 solution skeleton
"""

import logging
from argparse import ArgumentParser
from pathlib import Path


def parse_input(inputfile):
    rawdata = Path(inputfile).read_text('utf-8').splitlines()
    points = set()
    folds = []

    while rawdata:
        line = rawdata.pop(0)
        if not line:
            break
        points.add(tuple(map(int, line.split(','))))

    shape = (max(map(lambda x: x[0], points))+1, max(map(lambda x: x[1], points))+1)

    while rawdata:
        line = rawdata.pop(0)
        axis, coord = line.split(' ')[2].split('=')
        folds.append((axis, int(coord)))

    return points, shape, folds


def print_points(points, shape):
    data = [[0]*(shape[0]) for _ in range(shape[1])]

    for point in points:
        data[point[1]][point[0]] = 1

    for line in data:
        print(''.join(map(str, line)).replace('0', '.').replace('1', '#'))


def fold(points, shape, axis, coord):
    axis_index = 0 if axis == 'x' else 1

    folded_points = set()
    for point in points:
        if point[axis_index] < coord:
            folded_points.add(point)
            continue

        tmp = list(point)
        tmp[axis_index] = coord - (point[axis_index] - coord)
        folded_points.add(tuple(tmp))

    folded_shape = list(shape)
    folded_shape[axis_index] = int(folded_shape[axis_index] / 2)
    folded_shape = tuple(folded_shape)

    return folded_points, folded_shape


def main():
    """main"""

    parser = ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()
    logging.info(args)

    points, shape, folds = parse_input(args.input)

    print('## folding')
    for ifold in folds:
        points, shape = fold(points, shape, *ifold)

    print(f'dots {len(points)}')
    print_points(points, shape)


if __name__ == '__main__':
    main()
