#!/usr/bin/env python3
"""
aoc2021 solution skeleton
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

    data = Path(args.input).read_text('utf-8').splitlines()

    # digit vs number of segments
    decoder = {
        1: 2,
        4: 4,
        7: 3,
        8: 7,
    }
    
    known_lengths = decoder.values()
    result = 0
    for line in data:
        signals, segments = line.split(' | ')
        segments_lengths = list(map(len, segments.split()))
        for digit_len in segments_lengths:
            if digit_len in known_lengths:
                result += 1

    print(f'result {result}')


if __name__ == '__main__':
    main()
