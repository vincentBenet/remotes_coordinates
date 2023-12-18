import math
import random


def distance(target, source, error_offset=0, error_gain=0):
    dist_x = target[0] - source[0]
    dist_y = target[1] - source[1]
    dist_z = target[2] - source[2]
    dist = (
       dist_x ** 2 +
       dist_y ** 2 +
       dist_z ** 2
    ) ** 0.5
    print(f"1 {dist = }")
    dist += (2 * random.random() - 1) * error_gain * dist
    print(f"2 {dist = }")
    dist += (2 * random.random() - 1) * error_offset
    print(f"3 {dist = }")
    return dist


def distance2d(target, source, error_offset=0, error_gain=0):
    dist_x = target[0] - source[0]
    dist_y = target[1] - source[1]
    dist = (
       dist_x ** 2 +
       dist_y ** 2
    ) ** 0.5
    dist *= (2 * random.random() - 1) * error_gain
    dist += (2 * random.random() - 1) * error_offset
    return dist


def azimuth(target, source, error_offset=0):
    res_rad = math.pi / 2 - math.atan2(
        target[1] - source[1],
        target[0] - source[0])
    res_deg = res_rad * 180 / math.pi
    res_pos = res_deg + 360
    res_error = res_pos + random.random() * error_offset
    if res_error >= 360:
        res = res_error - 360
    else:
        res = res_error
    return res


def inclinaison(target, source, error_offset=0):
    return math.atan2(
        target[2] - source[2],
        (
            (target[0] - source[0]) ** 2 +
            (target[1] - source[1]) ** 2
        ) ** 0.5
    ) * 180 / math.pi + random.random() * error_offset


def random_point(d=1):
    return [1 - 2 * random.random() for _ in range(3)]


def random_set(n=100, d=1):
    return [random_point(d) for _ in range(n)][:n]


def points_set():
    return [
        [0, 0, 0],
        [1, 0, 0],
        [0, 1, 0],
        [1, 1, 0],
        [0, 0, 0],
        [-1, 0, 0],
        [0, -1, 0],
        [-1, -1, 0],
        [0, 0, 1],
        [1, 0, 1],
        [0, 1, 1],
        [1, 1, 1],
        [0, 0, 1],
        [-1, 0, 1],
        [0, -1, 1],
        [-1, -1, 1],
        [0, 0, -1],
        [1, 0, -1],
        [0, 1, -1],
        [1, 1, -1],
        [0, 0, -1],
        [-1, 0, -1],
        [0, -1, -1],
        [-1, -1, -1],
    ]