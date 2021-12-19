#!/usr/bin/env python3
"""
aoc2021 solution skeleton
"""

import logging
from argparse import ArgumentParser


class Pair:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return self.__str__()
    def __str__(self):
        return str([self.left, self.right])


def parse(value):
    if isinstance(value, int):
        return value
    if isinstance(value, list):
        return Pair(parse(value[0]), parse(value[1]))


def printInorder(root):
    if root:
        if isinstance(root, int):
            yield root
        else:
            for x in printInorder(root.left):
                yield x
            for x in printInorder(root.right):
                yield x


def main():
    """main"""

    parser = ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()
    logging.info(args)

    aa = Pair(3,2)
    bb = Pair(4, aa)
    print(aa)
    print(bb)

    ordered = list(printInorder(bb))
    print(ordered)
    breakpoint()


if __name__ == '__main__':
    main()
