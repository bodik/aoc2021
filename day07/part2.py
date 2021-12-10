#!/usr/bin/env python3
"""
aoc2021 solution skeleton
"""

import logging
from argparse import ArgumentParser
from pathlib import Path


def tri(val):
    return int((val*(val+1)) / 2)


def main():
    """main"""

    parser = ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()
    logging.info(args)

    data = list(map(int, Path(args.input).read_text('utf-8').strip().split(',')))

    fuels = []
    for align in range(max(data)):
        fuels.append(sum(tri(abs(x-align)) for x in data))

    fuel = min(fuels)
    align = fuels.index(fuel)
    print(f'align {align} fuel {fuel}')


if __name__ == '__main__':
    main()
