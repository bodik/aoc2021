#!/usr/bin/env python3
"""
xxx
"""

import logging
from argparse import ArgumentParser
from pathlib import Path


class Submarine:
    def __init__(self, h=0, d=0):
        self.h = h
        self.d = d

    def forward(self, val):
        self.h += val

    def up(self, val):
        self.d -= val

    def down(self, val):
        self.d += val

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
    submarine = Submarine()
    submarine.runprog(data)

    print(f'final position: h {submarine.h} d {submarine.d} -- mul: {submarine.h*submarine.d}')


if __name__ == '__main__':
    main()
