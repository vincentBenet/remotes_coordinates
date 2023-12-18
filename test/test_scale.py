

import os
import sys
import numpy

actual_dir = os.path.dirname(__file__)
repo_dir = os.path.join(actual_dir, "..")
sys.path.insert(0, repo_dir)

import remotes_coordinates
from remotes_coordinates import utils

EPS = 10e-1
RES = utils.random_point(d=100)

error_dist_offset = 2
error_dist_gain = 0.05
error_azimuth = 1
error_inclinaison = 1

print(RES)


def test_coordinates_distance():
    print(utils.random_set())
    assert utils.distance(RES, remotes_coordinates.calcul(numpy.array([
        p + [
            utils.distance(RES, p,
               error_offset=error_dist_offset,
               error_gain=error_dist_gain
            ),
            None,
            None
        ]
        for p in utils.random_set()
    ]))) < EPS


def test_coordinates_distance_nul():
    assert utils.distance(RES, remotes_coordinates.calcul(numpy.array([
        p + [utils.distance(RES, p,
               error_offset=error_dist_offset,
               error_gain=error_dist_gain
            ), None, None]
        for p in [RES] + utils.random_set(2)
    ]))) < EPS


def test_coordinates_azimuth():
    assert utils.distance2d(RES, remotes_coordinates.calcul(numpy.array([
        point + [None, utils.azimuth(RES, point, error_offset=error_azimuth), None]
        for point in utils.random_set()
    ]))) < EPS


def test_coordinates_distance_inclinaison():
    assert utils.distance(RES, remotes_coordinates.calcul(numpy.array([
        p + [utils.distance(RES, p,
               error_offset=error_dist_offset,
               error_gain=error_dist_gain
            ), None, utils.inclinaison(RES, p, error_offset=error_inclinaison)]
        for p in utils.random_set()
    ]))) < EPS


def test_coordinates_distance_azimuth_inclinaison():
    assert utils.distance(RES, remotes_coordinates.calcul(numpy.array([
        p + [utils.distance(RES, p,
               error_offset=error_dist_offset,
               error_gain=error_dist_gain
            ), utils.azimuth(RES, p, error_offset=error_azimuth), utils.inclinaison(RES, p, error_offset=error_inclinaison)]
        for p in utils.random_set(2)
    ]))) < EPS


def test_coordinates_azimuth_inclinaison():
    assert utils.distance(RES, remotes_coordinates.calcul(numpy.array([
        p + [None, utils.azimuth(RES, p, error_offset=error_azimuth), utils.inclinaison(RES, p, error_offset=error_inclinaison)]
        for p in utils.random_set()
    ]))) < EPS
