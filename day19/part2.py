"""
TODO: rotation matrixes are probably in somewhat wrong order given the axis ordering X, Y, Z


https://www.tutorialspoint.com/how-to-animate-a-scatter-plot-in-matplotlib
https://gist.githubusercontent.com/LyleScott/e36e08bfb23b1f87af68c9051f985302
https://www.meccanismocomplesso.org/en/3d-rotations-and-euler-angles-in-python/
https://stackoverflow.com/questions/38118598/3d-animation-using-matplotlib
https://matplotlib.org/stable/gallery/animation/simple_anim.html

https://www.euclideanspace.com/maths/algebra/matrix/transforms/examples/index.htm

https://www.brainm.com/software/pubs/math/Rotation_matrix.pdf
"""

import math as m
from argparse import ArgumentParser
from itertools import permutations
from copy import deepcopy
from pathlib import Path

import numpy as np


# consider plane rotation
# https://www.euclideanspace.com/maths/algebra/matrix/transforms/examples/index.htm
ROTATIONS = [
    (0, 0, 0),  (90, 0, 0), (180, 0, 0), (270, 0, 0),
    (0, 90, 0), (90, 90, 0), (180, 90, 0), (270, 90, 0),
    (0, 270, 0), (90, 270, 0), (180, 270, 0), (270, 270, 0),
    (0, 0, 90), (90, 0, 90), (180, 0, 90), (270, 0, 90),
    (0, 0, 180), (90, 0, 180), (180, 0, 180), (270, 0, 180),
    (0, 0, 270), (90, 0, 270), (180, 0, 270), (270, 0, 270)
]


def Rx(theta):  # pylint: disable=invalid-name
    return np.matrix([
        [1, 0, 0],
        [0, m.cos(theta), -m.sin(theta)],
        [0, m.sin(theta), m.cos(theta)]
    ])


def Ry(theta):  # pylint: disable=invalid-name
    return np.matrix([
        [m.cos(theta), 0, m.sin(theta)],
        [0, 1, 0],
        [-m.sin(theta), 0, m.cos(theta)]
    ])


def Rz(theta):  # pylint: disable=invalid-name
    return np.matrix([
        [m.cos(theta), -m.sin(theta), 0],
        [m.sin(theta), m.cos(theta), 0],
        [0, 0, 1]
    ])


def parse_input(inputfile):
    data = Path(inputfile).read_text('utf-8').splitlines()

    beacons = []
    tmp = []

    for line in data:
        if line.startswith('--- '):
            continue
        if not line:
            beacons.append(np.array(tmp, dtype=float))
            tmp = []
            continue
        tmp.append(list(map(int, line.split(','))))
    beacons.append(np.array(tmp, dtype=float))

    return beacons


def rotate(beacons, angles):
    phi, theta, psi = map(m.radians, angles)
    rotation_matrix = Rz(psi) * Ry(theta) * Rx(phi)
    tmp = deepcopy(beacons)
    for idx, point in enumerate(tmp):
        vec1 = np.array([point]).T
        vec2 = rotation_matrix * vec1
        # tmp[idx] = vec2.T
        tmp[idx] = np.round(vec2, decimals=1)[:, 0]

    return tmp


def check_alignment(base, beacons):
    """
    check number of matched points between base (beacon set) and beacons (another beacon set)
    """

    base_list = base.tolist()
    counter = 0
    for point in beacons.tolist():
        if point in base_list:
            counter += 1
    return counter


def realign(beacon1, beacon2):
    for point1 in beacon1:
        for point2 in beacon2:
            displacement = point2 - point1
            moved = beacon2 - displacement
            matched = check_alignment(beacon1, moved)
            if matched >= 12:
                return displacement, matched, moved
    return None, 0, None


def manhattan(point1, point2):
    return sum(abs(val1-val2) for val1, val2 in zip(point1, point2))


def main():
    np.set_printoptions(suppress=True)

    parser = ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('--animate', action='store_true')
    args = parser.parse_args()

    # beacons[scanner_id] = [[x, y, z], beacon, beacon, ...]
    beacons = parse_input(args.input)
    scanners = [(0, 0, 0)]

    universe = beacons.pop(0)
    while beacons:
        beacon = beacons.pop(0)
        for rotation in ROTATIONS:
            tmp = rotate(beacon, rotation)
            displacement, matched, realigned = realign(universe, tmp)
            if displacement is not None:
                scanners.append(tuple(displacement * np.array([-1, -1, -1])))
                print(f'realigned b:{beacon} r:{rotation} d:{displacement} m:{matched}')
                print(f'queue size {len(beacons)}')
                universe = np.unique(np.append(universe, realigned, axis=0), axis=0)
                break
        else:
            beacons.append(beacon)

    print('universe completed')
    print(universe.shape)
    print(universe)

    print('universe dump')
    with np.printoptions(threshold=np.inf):
        print(universe)

    print('universe size')
    print(max(manhattan(a, b) for (a, b) in permutations(scanners, 2)))


if __name__ == '__main__':
    main()
