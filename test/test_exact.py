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
POINTS = utils.points_set()


def test_coordinates_distance_xy():
    assert utils.distance(RES, remotes_coordinates.calcul(numpy.array([
        point + [utils.distance(RES, point), None, None]
        for point in POINTS
    ]))) < EPS


def test_coordinates_distance_xyz():
    assert utils.distance(RES, remotes_coordinates.calcul(numpy.array([
        point + [utils.distance(RES, point), None, None]
        for point in POINTS
    ]))) < EPS


def test_coordinates_azimuth():
    assert utils.distance2d(RES, remotes_coordinates.calcul(numpy.array([
        point + [None, utils.azimuth(target=RES, source=point), None]
        for point in utils.points_set()
    ]))) < EPS


def test_coordinates_distance_inclinaison():
        print(f"{RES = }")
        print(f"{utils.distance(target=[1, 1, 1], source=[-1, -1, -1]) = }")
        print(f"{utils.azimuth(target=[1, 1, 1], source=[-1, -1, -1]) = }")
        print(f"{utils.inclinaison(target=[1, 1, 1], source=[-1, -1, -1]) = }")
        assert utils.distance(RES, remotes_coordinates.calcul(numpy.array([
            point + [
                utils.distance(target=RES, source=point),
                None,
                utils.inclinaison(target=RES, source=point)]
            for point in POINTS
        ]))) < EPS


def test_coordinates_distance_azimuth_inclinaison():
    assert utils.distance(RES, remotes_coordinates.calcul(numpy.array([
        point + [
            utils.distance(target=RES, source=point),
            utils.azimuth(target=RES, source=point),
            utils.inclinaison(target=RES, source=point)]
        for point in POINTS
    ]))) < EPS


def test_coordinates_azimuth_inclinaison():
    assert utils.distance(RES, remotes_coordinates.calcul(numpy.array([
        point + [
            None,
            utils.azimuth(target=RES, source=point),
            utils.inclinaison(target=RES, source=point)]
        for point in utils.points_set()
    ]))) < EPS
