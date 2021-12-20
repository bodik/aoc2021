#!/usr/bin/env python3
"""
"""

import json
import logging
from argparse import ArgumentParser
from copy import deepcopy
from itertools import permutations
from math import ceil, floor
from pathlib import Path


class Node:
    def __init__(self, value, root=None):
        self.root = root
        self.value = value
        self.left = None
        self.right = None

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if self.value is not None:
            return str(self.value)
        return f'[{self.left}, {self.right}]'

    def iter(self):
        if self.left:
            for item in self.left.iter():
                yield item
        if self.value is not None:
            yield self
        if self.right:
            for item in self.right.iter():
                yield item

    @property
    def top(self):
        cur = self
        while cur.root:
            cur = cur.root
        return cur

    @property
    def depth(self):
        count = 0
        cur = self
        while cur.root:
            cur = cur.root
            count += 1
        return count

    def first_down_left(self):
        tmp = self
        while tmp.left:
            tmp = tmp.left
        return tmp

    def first_down_right(self):
        tmp = self
        while tmp.right:
            tmp = tmp.right
        return tmp

    def first_up_left(self):
        tmp = self.root
        ignore = self
        while tmp and (tmp.left is not None):
            if tmp.left != ignore:
                return tmp.left.first_down_right()
            ignore = tmp
            tmp = tmp.root
        return None

    def first_up_right(self):
        tmp = self.root
        ignore = self
        while tmp and (tmp.right is not None):
            if tmp.right != ignore:
                return tmp.right.first_down_left()
            ignore = tmp
            tmp = tmp.root
        return None

    def pred(self):
        return self.first_up_left()

    def succ(self):
        return self.first_up_right()


def parse(value, root=None):
    if isinstance(value, str):
        value = json.loads(value)

    if isinstance(value, int):
        return Node(value, root)

    if isinstance(value, list):
        new = Node(None, root)
        new.left = parse(value[0], new)
        new.right = parse(value[1], new)
        return new

    raise ValueError('invalid value')


def explode(data):
    for item in data.iter():
        if item.depth > 4:
            left = item
            right = item.succ()

            if left.pred():
                left.pred().value += left.value
            if right.succ():
                right.succ().value += right.value

            left.root.left = None
            left.root.right = None
            left.root.value = 0
            print(f'DEBUG: exploded {data}')
            return True, data

    return False, data


def split(data):
    for item in data.iter():
        if item.value > 9:
            item.left = Node(floor(item.value / 2), item)
            item.right = Node(ceil(item.value / 2), item)
            item.value = None
            print(f'DEBUG: splitted {data}')
            return True, data
    return False, data


def reduce(data):
    while True:
        change, data = explode(data)
        if change:
            continue

        change, data = split(data)
        if not change:
            break
    return data


def add(arg1, arg2):
    data = Node(None)
    data.left = deepcopy(arg1)
    data.right = deepcopy(arg2)
    data.left.root = data
    data.right.root = data
    return reduce(data)


def magnitude(data):
    if data.value is not None:
        return data.value
    return magnitude(data.left)*3 + magnitude(data.right)*2


def main():
    """main"""

    parser = ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()
    logging.info(args)

    data = list(map(parse, Path(args.input).read_text('utf-8').splitlines()))
    print(max(magnitude(add(a, b)) for (a, b) in permutations(data, 2)))


if __name__ == '__main__':
    main()
