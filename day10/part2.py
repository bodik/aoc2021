#!/usr/bin/env python3
"""
aoc2021 solution skeleton
"""

import logging
from argparse import ArgumentParser
from math import floor
from pathlib import Path


START_TERMS = '([{<'
END_TERMS = ')]}>'


def parse(text):
    stack = []

    for token in text:
        if token in START_TERMS:
            stack.append(token)

        if token in END_TERMS:
            if START_TERMS.index(stack[-1]) != END_TERMS.index(token):
                return stack, token
            stack.pop()

    return stack, None


def main():
    """main"""

    parser = ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()
    logging.info(args)

    data = Path(args.input).read_text('utf-8').splitlines()

    score_table = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4,
    }
    scores = []

    for line in data:
        stack, error_token = parse(line)
        if error_token:
            continue

        score = 0
        for item in [END_TERMS[START_TERMS.index(token)] for token in stack[::-1]]:
            score = score*5 + score_table[item]
        scores.append(score)

    scores = sorted(scores)
    final_score = scores[floor(len(scores)/2)]
    print(f'scores {scores}')
    print(f'final_score {final_score}')


if __name__ == '__main__':
    main()
