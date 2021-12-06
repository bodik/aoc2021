#!/usr/bin/env python3
"""
aoc2021 solution skeleton
"""

import logging
from argparse import ArgumentParser
from pathlib import Path


class Fish:
    def __init__(self, timer=8):
        self.timer = timer

    def tick(self):
        if self.timer == 0:
            self.timer = 6
            return True
        self.timer -= 1
        return False


def main():
    """main"""

    parser = ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('rounds', type=int)
    args = parser.parse_args()
    logging.info(args)

    data = Path(args.input).read_text()

    pool = [Fish(int(x)) for x in data.split(',')]

    for ctr in range(1, args.rounds+1):
        new = []
        for fish in pool:
            if fish.tick():
                new.append(Fish())

        pool += new
        print(f'round {ctr}: {[x.timer for x in pool]}')
    print(f'total {len(pool)}')


if __name__ == '__main__':
    main()
