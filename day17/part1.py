#!/usr/bin/env python3
"""
aoc2021 solution skeleton
"""

import logging
import re
from argparse import ArgumentParser
from collections import namedtuple
from pathlib import Path


Coords = namedtuple('Coords', 'x y')


def isin(point, target):
    if (
        (point.x >= target[0].x) and (point.y >= target[0].y)
        and (point.x <= target[1].x) and (point.y <= target[1].y)
    ):
        return True
    return False


def main():
    """main"""

    parser = ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()
    logging.info(args)

    data = Path(args.input).read_text('utf-8').strip()
    match = re.match(r'target area: x=(?P<x1>\d+)\.\.(?P<x2>\d+), y=(?P<y1>-?\d+)\.\.(?P<y2>-?\d+)', data)
    target = [Coords(int(match.group(1)), int(match.group(3))), Coords(int(match.group(2)), int(match.group(4)))]
    print(f'target {target}')

    best_maxy = 0
    best_velo = None
    best_step = 0

    for search_x in range(0, target[1].x+1):
        for search_y in range(target[0].y-1, 1000):

            # setup shot
            probe = Coords(0, 0)
            velo = Coords(search_x, search_y)
            initial_velo = Coords(search_x, search_y)
            max_y = 0

            # simulate
            for step in range(500):
                probe = Coords(probe.x+velo.x, probe.y+velo.y)
                velo = Coords(
                    velo.x + (0 if velo.x == 0 else (-1 if velo.x > 0 else 1)),
                    velo.y - 1
                )
                # print(f'step {step} probe {probe} velo {velo}')
                if probe.y > max_y:
                    max_y = probe.y
                if isin(probe, target):
                    if max_y > best_maxy:
                        best_maxy = max_y
                        best_velo = initial_velo
                        best_step = step
                    break

    print(f'best_maxy {best_maxy} best_velo {best_velo} step {best_step}')


if __name__ == '__main__':
    main()
