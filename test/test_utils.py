import os
import sys

actual_dir = os.path.dirname(__file__)
repo_dir = os.path.join(actual_dir, "..")
sys.path.insert(0, repo_dir)

from remotes_coordinates import utils


def test_distance():
    assert utils.distance([0, 0, 0], [0, 0, 0]) == 0
    assert utils.distance([0, 0, 0], [1, 1, 0]) == 2**0.5
    assert utils.distance([0, 0, 0], [1, 0, 0]) == 1
    assert utils.distance([0, 0, 0], [-1, 0, 0]) == 1
    assert utils.distance([0, 0, 0], [0, 1, 0]) == 1
    assert utils.distance([0, 0, 0], [0, -1, 0]) == 1
    assert utils.distance([0, 0, 0], [0, 0, 1]) == 1
    assert utils.distance([0, 0, 0], [0, 0, -1]) == 1
    assert utils.distance([0, 0, 0], [1, 1, 1]) == 3**0.5


def test_azimuth():
    assert utils.azimuth(source=[0, 0, 0], target=[0, 1, 0]) == 0
    assert utils.azimuth(source=[0, 0, 0], target=[1, 1, 1]) == 45
    assert utils.azimuth(source=[0, 0, 0], target=[1, 0, 0]) == 90
    assert utils.azimuth(source=[0, 1, 0], target=[0, 0, 0]) == 180
    assert utils.azimuth(source=[1, 1, 1], target=[0, 0, 0]) == 225
    assert utils.azimuth(source=[1, 0, 0], target=[0, 0, 0]) == 270


def test_inclinaison():
    assert utils.inclinaison(source=[0, 0, 0], target=[0, 1, 0]) == 0
    assert utils.inclinaison(source=[0, 0, 0], target=[1, 0, 0]) == 0
    assert utils.inclinaison(source=[0, 0, 0], target=[1, 1, 0]) == 0
    assert utils.inclinaison(source=[0, 0, 0], target=[0, 0, 1]) == 90
    assert utils.inclinaison(source=[0, 0, 0], target=[1, 0, 1]) == 45
    assert utils.inclinaison(source=[0, 0, 0], target=[0, 1, 1]) == 45
    assert utils.inclinaison(source=[0, 0, 0], target=[0, 0, -1]) == -90
    assert utils.inclinaison(source=[0, 0, 0], target=[1, 0, -1]) == -45
    assert utils.inclinaison(source=[0, 0, 0], target=[0, 1, -1]) == -45

