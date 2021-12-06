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
    parser.add_argument('rounds', type=int)
    args = parser.parse_args()
    logging.info(args)

    data = Path(args.input).read_text('utf-8')

    population = [0]*9
    for fish in data.split(','):
        population[int(fish)] += 1
    print(population)

    for _ in range(args.rounds):
        mothers = population.pop(0)
        population[6] += mothers
        population.append(mothers)

    print(f'total {sum(population)}')


if __name__ == '__main__':
    main()
