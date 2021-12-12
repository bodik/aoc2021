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
from collections import defaultdict
from pathlib import Path
from pprint import pprint


def bfs(graph, start, end):
    all_paths = []

    queue = []
    queue.append([start])

    while queue:
        path = queue.pop(0)
        node = path[-1]
        if node == end:
            all_paths.append(path)
            continue
        for adjacent in graph.get(node, []):
            if adjacent.islower() and (adjacent in path):
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
    print(paths)
    print(len(paths))


if __name__ == '__main__':
    main()
