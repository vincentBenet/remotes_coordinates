import os
import sys
import numpy

actual_dir = os.path.dirname(__file__)
repo_dir = os.path.join(actual_dir, "..")
sys.path.insert(0, repo_dir)

import remotes_coordinates
from remotes_coordinates import utils

EPS = 10e-2
RES = [1, 1, 1]


def test_coordinates_distance_xy():
    assert utils.distance(RES, remotes_coordinates.calcul(numpy.array([
        p + [utils.distance(RES, p), None, None]
        for p in [
            [0, 0, 1],
            [1, 0, 1],
            [0, 1, 1],
        ]
    ]))) < EPS


def test_coordinates_distance_xyz():
    assert utils.distance(RES, remotes_coordinates.calcul(numpy.array([
        point + [utils.distance(RES, point), None, None]
        for point in [
            [0, 0, 0],
            [0, 1, 0],
            [1, 1, 0],
            [0, 0, 1],
        ]
    ]))) < EPS


def test_coordinates_azimuth():
    assert utils.distance2d(RES, remotes_coordinates.calcul(numpy.array([
        point + [None, utils.azimuth(target=RES, source=point), None]
        for point in [
            [0, 0, 0],
            [0, 1, 0],
        ]
    ]))) < EPS


def test_coordinates_distance_inclinaison():
        assert utils.distance(RES, remotes_coordinates.calcul(numpy.array([
            point + [
                utils.distance(target=RES, source=point),
                utils.azimuth(target=RES, source=point),
                None]
            for point in [
                [0, 0, 0],
                [0, 1, 1],
            ]
        ]))) < EPS


def test_coordinates_distance_azimuth_inclinaison():
    point = [0, 0, 0]
    print()
    print(f"{utils.distance(target=RES, source=point) = }")
    print(f"{utils.azimuth(target=RES, source=point) = }")
    print(f"{utils.inclinaison(target=RES, source=point) = }")
    assert utils.distance(RES, remotes_coordinates.calcul(numpy.array([
        point + [
            utils.distance(target=RES, source=point),
            utils.azimuth(target=RES, source=point),
            utils.inclinaison(target=RES, source=point)]
        for point in [
            [0, 0, 0],
        ]
    ]))) < EPS


def test_coordinates_azimuth_inclinaison():
    assert utils.distance(RES, remotes_coordinates.calcul(numpy.array([
        point + [
            None,
            utils.azimuth(target=RES, source=point),
            utils.inclinaison(target=RES, source=point)]
        for point in [
            [0, 0, 0],
            [1, 0, 0],
        ]
    ]))) < EPS
