import os
import sys
import numpy

actual_dir = os.path.dirname(__file__)
repo_dir = os.path.join(actual_dir, "..")
sys.path.insert(0, repo_dir)

import remotes_coordinates
from remotes_coordinates import utils

EPS = 10e-2
RES = utils.random_point()
print(RES)


def test_coordinates_distance():
    assert utils.distance(RES, remotes_coordinates.calcul(numpy.array([
        p + [
            utils.distance(RES, p),
            None,
            None
        ]
        for p in utils.random_set()
    ]))) < EPS


def test_coordinates_azimuth():
    assert utils.distance2d(RES, remotes_coordinates.calcul(numpy.array([
        point + [None, utils.azimuth(RES, point), None]
        for point in utils.random_set()
    ]))) < EPS


def test_coordinates_distance_inclinaison():
    assert utils.distance(RES, remotes_coordinates.calcul(numpy.array([
        p + [utils.distance(RES, p), None, utils.inclinaison(RES, p)]
        for p in utils.random_set()
    ]))) < EPS


def test_coordinates_distance_azimuth_inclinaison():
    assert utils.distance(RES, remotes_coordinates.calcul(numpy.array([
        p + [utils.distance(RES, p), utils.azimuth(RES, p), utils.inclinaison(RES, p)]
        for p in utils.random_set()
    ]))) < EPS


def test_coordinates_azimuth_inclinaison():
    assert utils.distance(RES, remotes_coordinates.calcul(numpy.array([
        p + [None, utils.azimuth(RES, p), utils.inclinaison(RES, p)]
        for p in utils.random_set()
    ]))) < EPS
