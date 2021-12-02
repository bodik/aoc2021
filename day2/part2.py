#!/usr/bin/env python3
"""
xxx
"""

import logging
from argparse import ArgumentParser
from pathlib import Path


class Submarine:
    def __init__(self, horiz=0, depth=0, aim=0):
        self.horiz = horiz
        self.depth = depth
        self.aim = aim

    def forward(self, val):
        self.horiz += val
        self.depth += self.aim * val

    def up(self, val):  # pylint: disable=invalid-name
        self.aim -= val

    def down(self, val):
        self.aim += val

    def runprog(self, prog):
        for step in prog.splitlines():
            move, value = step.split()
            if hasattr(self, move):
                getattr(self, move)(int(value))
            else:
                raise RuntimeError('invalid program')


def main():
    """main"""

    parser = ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()
    logging.info(args)

    data = Path(args.input).read_text('utf-8')
    sub = Submarine()
    sub.runprog(data)

    print(f'final position: horiz {sub.horiz} d {sub.depth} -- mul: {sub.horiz*sub.depth}')


if __name__ == '__main__':
    main()
