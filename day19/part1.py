"""
https://www.tutorialspoint.com/how-to-animate-a-scatter-plot-in-matplotlib
https://gist.githubusercontent.com/LyleScott/e36e08bfb23b1f87af68c9051f985302
https://www.meccanismocomplesso.org/en/3d-rotations-and-euler-angles-in-python/
https://stackoverflow.com/questions/38118598/3d-animation-using-matplotlib
https://matplotlib.org/stable/gallery/animation/simple_anim.html

https://www.euclideanspace.com/maths/algebra/matrix/transforms/examples/index.htm
"""

import math as m
from argparse import ArgumentParser
from itertools import permutations
from copy import deepcopy
from itertools import cycle
from pathlib import Path
from time import sleep

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D


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

ROTATIONS_CYCLE = cycle(ROTATIONS)

#SPACE = (-3, 3)
SPACE = (-1200, 1200)


def Rx(theta):
    return np.matrix([
        [ 1, 0           , 0           ],
        [ 0, m.cos(theta),-m.sin(theta)],
        [ 0, m.sin(theta), m.cos(theta)]
    ])
  
def Ry(theta):
    return np.matrix([
        [ m.cos(theta), 0, m.sin(theta)],
        [ 0           , 1, 0           ],
        [-m.sin(theta), 0, m.cos(theta)]
    ])
  
def Rz(theta):
    return np.matrix([
        [ m.cos(theta), -m.sin(theta), 0 ],
        [ m.sin(theta), m.cos(theta) , 0 ],
        [ 0           , 0            , 1 ]
    ])


def rotation_matrix(phi=0.1, theta=0, psi=0):
    """
    angle should be ? [0, 2*m.pi] rad
    """
    return Rx(phi) * Ry(theta) * Rz(psi)


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
    rotx, roty, rotz = angles
    R = rotation_matrix(m.radians(rotx), m.radians(roty), m.radians(rotz))
    tmp = deepcopy(beacons)
    for idx, point in enumerate(tmp):
        v1 = np.array([point]).T
        v2 = R * v1
        #tmp[idx] = v2.T
        tmp[idx] = np.round(v2, decimals=1)[:,0]

    return tmp


def check_alignment(base, beacons):
    """
    check number of matched points between base and beacons
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


def main():
    np.set_printoptions(suppress=True)

    parser = ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('--animate', action='store_true')
    args = parser.parse_args()

    # beacons[scanner_id] = [[x, y, z], beacon, beacon, ...]
    beacons = parse_input(args.input)

    universe = beacons.pop()
    while beacons:
        beacon = beacons.pop()
        for rotation in ROTATIONS:
            tmp = rotate(beacon, rotation)
            displacement, matched, realigned = realign(universe, tmp)
            if displacement is not None:
                print(f'realigned b:{beacon} r:{rotation} d:{displacement} m:{matched}')
                print(f'queue size {len(beacons)}')
                universe = np.unique(np.append(universe, realigned, axis=0), axis=0)
                break
        else:
            beacons.insert(0, beacon)

    print('universe completed')
    print(universe.shape)
    print(universe)

    print('universe dump')
    with np.printoptions(threshold=np.inf):
        print(universe)


if __name__ == '__main__':
    main()
