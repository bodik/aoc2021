#!/usr/bin/env python3
"""
https://en.wikipedia.org/wiki/Zipper_(data_structure)
"""

import json
import logging
from argparse import ArgumentParser
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
            for x in self.left.iter():
                yield x
        if self.value is not None:
            yield self
        if self.right:
            for x in self.right.iter():
                yield x

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

    def pred(self):
        alist = list(self.top.iter())
        index = alist.index(self)
        if index > 0:
            return alist[index-1]
        return None

    def succ(self):
        alist = list(self.top.iter())
        index = alist.index(self)
        if index < len(alist)-1:
            return alist[index+1]
        return None


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


def add(x, y):
    data = Node(None)
    data.left = x
    data.right = y
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

    #data = json.loads("[[6,[5,[4,[3,2]]]],[6,[5,[4,[3,2]]]]]")
    data = json.loads("[[6,[5,[4,[3,2]]]],1]")
    tree = parse(data, None)
    print(tree)

    tree = parse(json.loads('[[1,2],3]'), None)
    treelist = list(tree.iter())

    tree = parse(json.loads('[[[[[9,8],1],2],3],4]'), None)
    print(tree)
    print(explode(tree))

    tree = parse(json.loads('[7,[6,[5,[4,[3,2]]]]]'), None)
    print(tree)
    print(explode(tree))

    tree = parse(json.loads('[[6,[5,[4,[3,2]]]],1]'), None)
    print(tree)
    print(explode(tree))

    tree = parse(json.loads('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]'), None)
    print(tree)
    print(explode(tree))

    print(split(Node(10)))
    print(split(Node(11)))

    print(add(parse('[[[[4,3],4],4],[7,[[8,4],9]]]'), parse('[1,1]')))

    print('------------')

    data = list(map(parse, Path(args.input).read_text('utf-8').splitlines()))
    result = data.pop(0)
    for item in data:
        result = add(result, item)
        print(result)
    print(f'sumresult {result}')
    print(magnitude(result))


if __name__ == '__main__':
    main()
