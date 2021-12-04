#!/usr/bin/env python3
"""
aoc2021 solution skeleton
"""

import logging
from argparse import ArgumentParser
from pathlib import Path

import numpy as np


class Board:
    def __init__(self, data):
        self.data = np.array(data)

    def __str__(self):
        out = ''
        for line in self.data:
            out += '%s\n' % line
        return out

    def mark(self, value):
        """mark value on board"""

        found = np.where(self.data == value)
        if found:
            self.data[found] = -1
            return True
        return False

    def check(self):
        """check if board has won in current state"""

        for row in self.data:
            if all(x == -1 for x in row):
                return True
        for col in self.data.transpose():
            if all(x == -1 for x in col):
                return True
        return False

    def score(self, val):
        """compute final board score"""

        counter = 0
        for row in self.data:
            counter += sum(map(int, filter(lambda x: x != -1, row)))
        return counter * val



def parse_input(input_path):
    data = Path(input_path).read_text('utf-8').splitlines()

    draw_buf = list(map(int, data.pop(0).split(',')))
    data.pop(0) # empty separator

    boards = []
    tmp = []

    for line in data:
        if not line:
            boards.append(Board(tmp))
            tmp = []
            continue
        tmp.append(list(map(int, line.split())))
    if tmp:
        boards.append(Board(tmp))

    return draw_buf, boards


def check_boards(boards, draw):
    """
    check all boards for draw value

    returns: boards, winner or None
    """

    for board in boards:
        if board.mark(draw):
            if board.check():
                return boards, board

    return boards, None


def main():
    """main"""

    parser = ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()
    logging.info(args)

    draw_buf, boards = parse_input(args.input)
    
    print(draw_buf)
    for idx, board in enumerate(boards):
        print(idx)
        print(board)

    for draw in draw_buf:
        boards, winner = check_boards(boards, draw)
        if winner:
            print('winner')
            print(winner)
            print(winner.score(draw))
            break



if __name__ == '__main__':
    main()
