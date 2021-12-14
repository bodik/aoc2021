#!/usr/bin/env python3
"""
aoc2021 solution skeleton
"""

import logging
from argparse import ArgumentParser
from copy import deepcopy
from collections import defaultdict
from itertools import tee
from pathlib import Path


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    aaa, bbb = tee(iterable)
    next(bbb, None)
    return zip(aaa, bbb)


def parse_input(inputfile):
    data = Path(inputfile).read_text('utf-8').splitlines()
    template = data.pop(0)
    data.pop(0)  # drop empty line
    rules = dict([line.split(' -> ') for line in data])
    return template, rules


def main():
    """main"""

    parser = ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('steps', type=int)
    args = parser.parse_args()
    logging.info(args)

    template, rules = parse_input(args.input)
    print(template)
    print(rules)

    counter = defaultdict(int)
    for pair in map(''.join, pairwise(template)):
        counter[pair] += 1

    for step in range(args.steps):
        print(f'step {step}')
        new_counter = deepcopy(counter)
        for pair in counter:
            if pair in rules:
                new_counter[pair] -= counter[pair]
                new_counter[f'{pair[0]}{rules[pair]}'] += counter[pair]
                new_counter[f'{rules[pair]}{pair[1]}'] += counter[pair]
        counter = new_counter

    length = sum(counter.values())+1
    print(f'length {length}')

    final_counter = defaultdict(int)
    for key, val in counter.items():
        final_counter[key[0]] += val
    final_counter[template[-1]] += 1
    final_counter_sorted = sorted(final_counter, key=final_counter.get, reverse=True)
    print(f'result {final_counter[final_counter_sorted[0]] - final_counter[final_counter_sorted[-1]]}')


if __name__ == '__main__':
    main()
