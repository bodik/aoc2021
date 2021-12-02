#!/usr/bin/env python3
"""
day1 part1
"""

import logging
from argparse import ArgumentParser
from pathlib import Path


def main():
    """main"""

    parser = ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()
    logging.info(args)

    data = list(map(int, Path(args.input).read_text('utf-8').splitlines()))

    data1 = [sum(data[i:i+3]) for i in range(len(data)-2)]
    data = data1

    counter = 0
    prev = data.pop(0)
    for item in data:
        if item > prev:
            counter += 1
        prev = item

    print(f'counter: {counter}')


if __name__ == '__main__':
    main()
