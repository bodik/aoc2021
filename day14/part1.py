#!/usr/bin/env python3
"""
aoc2021 solution skeleton
"""

import logging
from argparse import ArgumentParser
from collections import Counter
from itertools import tee
from pathlib import Path
from time import time


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


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

    new_template = ''
    for step in range(args.steps):
        print(f'step {step}')
        stime = time()
        new_template = ''
        for pair in map(''.join, pairwise(template)):
            new_template += pair[0]
            if pair in rules:
                new_template += rules[pair]
        new_template += template[-1]
        template = new_template
        print(template)
        #print(f'step {step} {time() - stime}')

    print(f'steps {step}')
    print(f'template len {len(template)}')
    counter = Counter(template)
    counter_sorted = sorted(counter, key=counter.get, reverse=True)
    print(f'result {counter[counter_sorted[0]] - counter[counter_sorted[-1]]}')


if __name__ == '__main__':
    main()
