#!/usr/bin/env python3
"""
let's make proper non-recursion solution based on Bread-First Search

* http://en.wikipedia.org/wiki/Breadth-first_search
* https://stackoverflow.com/a/8922151/8326867

```
# graph is in adjacent list representation
graph = {
        '1': ['2', '3', '4'],
        '2': ['5', '6'],
        '5': ['9', '10'],
        '4': ['7', '8'],
        '7': ['11', '12']
        }

def bfs(graph, start, end):
    # maintain a queue of paths
    queue = []
    # push the first path into the queue
    queue.append([start])
    while queue:
        # get the first path from the queue
        path = queue.pop(0)
        # get the last node from the path
        node = path[-1]
        # path found
        if node == end:
            return path
        # enumerate all adjacent nodes, construct a
        # new path and push it into the queue
        for adjacent in graph.get(node, []):
            new_path = list(path)
            new_path.append(adjacent)
            queue.append(new_path)

print bfs(graph, '1', '11')
```
"""

import logging
from argparse import ArgumentParser
from collections import deque, defaultdict, Counter
from pathlib import Path
from pprint import pprint


def bfs(graph, start, end):
    """
    After reviewing the available paths (part1), you realize you might have time to
    visit a single small cave twice. Specifically, big caves can be visited any
    number of times, a single small cave can be visited at most twice, and the
    remaining small caves can be visited at most once. However, the caves named
    start and end can only be visited exactly once each: once you leave the
    start cave, you may not return to it, and once you reach the end cave, the
    path must end immediately.
    """

    all_paths = []

    queue = deque()  # deque is required. it's fast for both ends.
    queue.append([start])

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == end:
            all_paths.append(path)
            continue

        for adjacent in graph.get(node, []):
            if adjacent == 'start':
                continue

            if adjacent.islower() and (adjacent in path):
                counter = {k: v for k, v in Counter(path).items() if k.islower()}
                if len(list(filter(lambda x: x[1] == 2, counter.items()))) == 1:
                    continue

            new_path = list(path)
            new_path.append(adjacent)
            queue.append(new_path)

    return all_paths


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
    paths = bfs(graph, 'start', 'end')
    print(len(paths))


if __name__ == '__main__':
    main()
