#!/usr/bin/env python3
"""
aoc2021 solution skeleton
"""

import logging
import operator
from argparse import ArgumentParser
from copy import deepcopy
from pathlib import Path
from time import time

import numpy as np


def parse_input(inputfile):
    data = Path(inputfile).read_text('utf-8').splitlines()
    algo = data.pop(0)
    data.pop(0)  # drop empty line

    image = set()
    for row in range(len(data)):
        for col in range(len(data[row])):
            if data[row][col] == '#':
                image.add((row, col))

    return algo, image


def get_points(point):
    points = []
    for vector in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]:
        tmp = tuple(map(operator.add, point, vector))
        points.append(tmp)
    return points


def print_image(image):
    image = list(image)

    min_row = min(x[0] for x in image)
    min_col = min(x[1] for x in image)

    if min_row < 0:
        offset = abs(min_row)
        for idx in range(len(image)):
            image[idx] = (image[idx][0] + offset, image[idx][1])

    if min_col < 0:
        offset = abs(min_col)
        for idx in range(len(image)):
            image[idx] = (image[idx][0], image[idx][1] + offset)

    max_row = max(x[0] for x in image)
    max_col = max(x[1] for x in image)

    tmp = np.full((max_row+1, max_col+1), '.')
    for item in image:
        tmp[item] = '#'

    for line in tmp:
        print(''.join(line))


def enhance(image, algo, default=0):
    new_image = set()

    min_row = min(x[0] for x in image)
    min_col = min(x[1] for x in image)
    max_row = max(x[0] for x in image)
    max_col = max(x[1] for x in image)

    for row in range(min_row-1, max_row+2):
        for col in range(min_col-1, max_col+2):
            point = (row, col)
            value = ''
            for adj in get_points(point):
                if (adj[0] >= min_row) and (adj[0] <= max_row) and (adj[1] >= min_col) and (adj[1] <= max_col):
                    value += '1' if adj in image else '0'
                else:
                    value += str(default)
            value = int(value, base=2)
            if algo[value] == '#':
                new_image.add(point)

    return new_image


def main():
    """main"""

    parser = ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()
    logging.info(args)

    algo, image = parse_input(args.input)
    print_image(image)

    print('===========')
    default = 0
    for i in range(50):
        start = time()
        print(f'round {i} ..', end='')
        image = enhance(image, algo, default)
        if algo[0] == '#':
            default = int(not(default))
        print(f'{time()-start}s')

    print_image(image)
    print(f'pixels {len(image)}')


if __name__ == '__main__':
    main()
