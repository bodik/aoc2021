#!/usr/bin/env python3
"""
https://en.wikipedia.org/wiki/Zipper_(data_structure)
"""

import json
import logging
from argparse import ArgumentParser


class Node:
    def __init__(self, value, root, left=None, right=None):
        self.root = root
        self.value = value
        self.left = left
        self.right = right

    def path(self):
        ret = 0
        cur = self
        while cur:
            ret += 1
            cur = cur.root
        return ret - 1

    def __repr__(self):
        return self.__str__()
    def __str__(self):
        if self.value:
            return str(self.value)
        return str([self.left, self.right])


def parse(value, root):

    if isinstance(value, int):
        return Node(value, root)

    if isinstance(value, list):
        new = Node(None, root)
        new.left = parse(value[0], new)
        new.right = parse(value[1], new)
        return new


# A function to do inorder tree traversal
def printInorder(root):
    if root:
        for x in printInorder(root.left):
            yield x
        if root.value:
            yield root
        for x in printInorder(root.right):
            yield x


def main():
    """main"""

    parser = ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()
    logging.info(args)

    #data = json.loads("[[6,[5,[4,[3,2]]]],[6,[5,[4,[3,2]]]]]")
    data = json.loads("[[6,[5,[4,[3,2]]]],1]")

    tree = parse(data, None)

    mylist = list(printInorder(tree))
    breakpoint()


if __name__ == '__main__':
    main()
