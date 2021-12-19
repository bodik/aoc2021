#!/usr/bin/env python3
"""
aoc2021 solution skeleton
"""

import logging
from argparse import ArgumentParser
from pathlib import Path
from math import ceil, floor


class Item:
    def __init__(self, depth, value):
        self.depth = depth
        self.value = value

    def __repr__(self):
#        return f'<d:{self.depth} {self.value}>'
        return f'{self.value}'


def parse(data):
    ptr = 0
    end = len(data)

    result = []
    depth = 0

    while ptr < end:
        if data[ptr] == '[':
            depth += 1

        elif data[ptr] == ']':
            depth -= 1

        elif data[ptr] == ',':
            pass

        elif (data[ptr] >= '0') and (data[ptr] <= '9'):
            result.append(Item(depth, int(data[ptr])))

        else:
            raise ValueError('invalid data')

        ptr += 1

    return result



def explode(data):
    ptr = 0
    while ptr < len(data):
        # explode
        if data[ptr].depth > 4:
            left = data[ptr]
            right = data.pop(ptr+1)
            prev_index = ptr - 1
            succ_index = ptr + 1

            if prev_index >= 0:
                data[prev_index].value += left.value

            if succ_index < len(data):
                data[succ_index].value += right.value
       
            data[ptr].depth -= 1
            data[ptr].value = 0
            print(f'explode {data}')
        ptr += 1
    return data


def reduce(data):

    # find exploded
    ptr = 0
    
    while ptr < len(data):

        data = explode(data)

        # split
        if data[ptr].value > 9:
            newl = Item(data[ptr].depth+1, floor(data[ptr].value / 2))
            newr = Item(data[ptr].depth+1, ceil(data[ptr].value / 2))
            data[ptr] = newr
            data.insert(ptr, newl)
            ptr = 0
            print(f'split {data}')
            continue

        # move forward
        ptr +=1 

    return data


def magnitude(data):

    print(f'magnitude {data}')

    while len(data) > 1:
        ptr = 0
        while ptr < len(data)-1:
            if data[ptr].depth != data[ptr+1].depth:
                ptr += 1
                continue

            # implode
            new = Item(data[ptr].depth-1, data[ptr].value*3 + data[ptr+1].value*2)
            data.pop(ptr)
            data[ptr] = new
            ptr += 1

    return data


def add(itemx, itemy):
    print('add------')
    print(f'itemx {itemx}')
    print(f'itemy {itemy}')

    result = itemx + itemy
    ptr = 0
    while ptr < len(result):
        result[ptr].depth += 1
        ptr += 1
    return reduce(result)


def main():
    """main"""

    parser = ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()
    logging.info(args)

#    # parsing tests
#    data = '[[1,2],3]'
#    print(data)
#    print(parse(data))
#    data = '[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]'
#    print(data)
#    print(parse(data))
#
#    # reduces
#    data = '[[[[[9,8],1],2],3],4]'
#    print(data)
#    print(reduce(parse(data)))
#    data = '[7,[6,[5,[4,[3,2]]]]]'
#    print(data)
#    print(reduce(parse(data)))
#    data = '[[6,[5,[4,[3,2]]]],1]'
#    print(data)
#    print(reduce(parse(data)))
#    data = '[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]'
#    print(data)
#    print(reduce(parse(data)))
#
#    # addition
#    print(add(parse('[[[[4,3],4],4],[7,[[8,4],9]]]'), parse('[1,1]')))

    print('----------')
    data = Path(args.input).read_text('utf-8').splitlines()
    result = parse(data.pop(0))
    for item in data:
        result = add(result, parse(item))
        print(result)

    print(f'sumresult {result}')
    print(magnitude(result))


if __name__ == '__main__':
    main()
