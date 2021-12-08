#!/usr/bin/env python3
"""
aoc2021 solution skeleton
"""

import logging
from argparse import ArgumentParser
from collections import Counter
from pathlib import Path


def construct_decoder(signals):
    """
    infer decoder from signals

      0:      1:      2:      3:      4:
     aaaa    ....    aaaa    aaaa    ....
    b    c  .    c  .    c  .    c  b    c
    b    c  .    c  .    c  .    c  b    c
     ....    ....    dddd    dddd    dddd
    e    f  .    f  e    .  .    f  .    f
    e    f  .    f  e    .  .    f  .    f
     gggg    ....    gggg    gggg    ....

      5:      6:      7:      8:      9:
     aaaa    aaaa    aaaa    aaaa    aaaa
    b    .  b    .  .    c  b    c  b    c
    b    .  b    .  .    c  b    c  b    c
     dddd    dddd    ....    dddd    dddd
    .    f  e    f  .    f  e    f  .    f
    .    f  e    f  .    f  e    f  .    f
     gggg    gggg    ....    gggg    gggg

    # phase 0 - identify segments by unique properties
    a 8x
    b 6x *
    c 8x
    d 7x
    e 4x *
    f 9x *
    g 7x

    # phase 1
    1. exactly 2 wires
    4. exactly 4 wires
    7. exactly 3 wires
    8. all wires

    # phase 2
    9. 8 - segment_e
    3. 9 - segment_b
    2. 3 - segment_f + segment_e

    # phase 3
    5. exactly 5 wires

    # phase 4
    0. in which remaining item is included digit_1

    # phase 5
    6. remainder
    """

    decoder = {}

    # phase 0 -- segments by unique counts
    tmp = Counter(''.join(signals))
    segment_b = next(filter(lambda x: x[1] == 6, tmp.items()))[0]
    segment_e = next(filter(lambda x: x[1] == 4, tmp.items()))[0]
    segment_f = next(filter(lambda x: x[1] == 9, tmp.items()))[0]

    # phase1 -- digits via unique counts
    decoder[1] = next(filter(lambda x: len(x) == 2, signals))
    decoder[4] = next(filter(lambda x: len(x) == 4, signals))
    decoder[7] = next(filter(lambda x: len(x) == 3, signals))
    decoder[8] = next(filter(lambda x: len(x) == 7, signals))
    for item in decoder.values():
        signals.remove(item)

    # phase 2 -- digits and segments (de)combinations
    decoder[9] = decoder[8].replace(segment_e, '')
    signals.remove(decoder[9])
    decoder[3] = decoder[9].replace(segment_b, '')
    signals.remove(decoder[3])
    decoder[2] = ''.join(sorted(decoder[3].replace(segment_f, '') + segment_e))
    signals.remove(decoder[2])

    # phase 3 -- digits via unique counts
    decoder[5] = next(filter(lambda x: len(x) == 5, signals))
    signals.remove(decoder[5])

    # phase 4 -- in which remaining item is included digit_1
    for item in signals:
        if all(x in item for x in decoder[1]):
            decoder[0] = item
    signals.remove(decoder[0])

    # phase 5 -- remainder
    decoder[6] = signals[0]

    return {val: key for key, val in decoder.items()}


def main():
    """main"""

    parser = ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()
    logging.info(args)

    data = Path(args.input).read_text('utf-8').splitlines()

    total = 0
    for line in data:
        signals, segments = list(map(str.split, line.split(' | ')))
        signals = list(map(lambda x: ''.join(sorted(x)), signals))
        segments = list(map(lambda x: ''.join(sorted(x)), segments))

        decoder = construct_decoder(signals)
        total += int(''.join(str(decoder[item]) for item in segments))

    print(f'total {total}')


if __name__ == '__main__':
    main()
