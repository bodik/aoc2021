#!/usr/bin/env python3
"""
aoc2021 solution skeleton
"""

import logging
from argparse import ArgumentParser
from pathlib import Path


def parse(text):
    stack = []
    START_TERMS = '([{<'
    END_TERMS = ')]}>'

    for token in text:
        if token in START_TERMS:
            stack.append(token)

        if token in END_TERMS:
            if START_TERMS.index(stack[-1]) != END_TERMS.index(token):
                return token
            stack.pop()

    return None


def main():
    """main"""

    parser = ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()
    logging.info(args)

    data = Path(args.input).read_text('utf-8').splitlines()

    score = 0
    score_table = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137,
    }

    for line in data:
        tmp = parse(line)
        if tmp:
            score += score_table[tmp]

    print(f'score {score}')


if __name__ == '__main__':
    main()
