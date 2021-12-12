#!/usr/bin/env python3
"""
aoc2021 solution skeleton
"""

import logging
from argparse import ArgumentParser
from collections import defaultdict, Counter
from pathlib import Path
from pprint import pprint


def find_all_paths(graph, start, end, path=[]):
    path = path + [start]

    if start == end:
        return [path]

    if start not in graph:
        return []

    paths = []
    for node in graph[start]:
        if (node in path) and node.islower():
            continue

        for xpath in find_all_paths(graph, node, end, path):
            paths.append(xpath)

    return paths


def main():
    """main"""

    parser = ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()
    logging.info(args)

    data = Path(args.input).read_text('utf-8').splitlines()

    graph = defaultdict(set)
    for start, end in [x.split('-') for x in data]:
        graph[start].add(end)
        graph[end].add(start)

    pprint(graph)
    paths = find_all_paths(graph, 'start', 'end')
    print(paths)
    print(len(paths))


if __name__ == '__main__':
    main()
