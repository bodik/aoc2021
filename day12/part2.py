#!/usr/bin/env python3
"""
definitely not nice solution
"""

import logging
from argparse import ArgumentParser
from collections import defaultdict, Counter
from pathlib import Path
from pprint import pprint


def find_all_paths(graph, start, end, path=None):
    if not path:
        path = []

    path = path + [start]

    if start == end:
        return [path]

    if start not in graph:
        return []

    paths = []
    for node in graph[start]:
        if node == 'start':
            continue

        if (node in path) and node.islower():
            counter = [v for k, v in Counter(path).items() if (k.islower() and v > 1)]
            if len(counter) > 1:
                continue
            if counter and (counter[0] == 2):
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
    print(len(paths))


if __name__ == '__main__':
    main()
