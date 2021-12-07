#!/usr/bin/env python3
"""
aoc2021 solution skeleton
"""

import logging
from argparse import ArgumentParser
from pathlib import Path
from statistics import median


def main():
    """main"""

    parser = ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()
    logging.info(args)

    data = list(map(int, Path(args.input).read_text().strip().split(',')))
    align = int(median(data))
    fuel = sum(abs(x-align) for x in data)
    print(f'align {align} fuel {fuel}')


if __name__ == '__main__':
    main()
