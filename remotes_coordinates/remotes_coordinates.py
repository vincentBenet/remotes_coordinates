import itertools
import sys

import numpy
import math
from scipy.optimize import minimize as scipy_optimize_minimize
import matplotlib.pyplot as plt
from . import utils

TYPE_POINT = list[float, float, float | None, float | None, float | None, float | None]
TYPE_POINTS = numpy.ndarray
TYPE_RES = list[float, float, float]


def minimize(
    points: TYPE_POINTS,
    n:int = 3,
) -> TYPE_RES:
    """
    Take input points and measure to find the researched point.
    This minimisation problem is a 3x3 -> 3
        There is 3 fixed inputs for each point (X, Y, Z) and 3 measures (Distance, Azimuth, Inclinaison)
        The output is 3 values (X, Y, Z) of the target to find
    This function will guess the target coordinates based on the input points and measures
    :param points: array of points [x, y, z, d, a, i]
        x: Coordinate X in meter of the input point
        y: Coordinate Y in meter of the input point
        z: Coordinate Z in meter of the input point
        d (opt): Distance from input point to the target in meter, None if unknow
        a (opt): Azimuth from input point to the target in degree, None if unknow
        i (opt): Inclinaison (vertical angle) from input point to the target in degree, None if unknow
    :return: result_point, points
        result_point [res_x, res_y, res_z]
            res_x: coordinates X of target in meter
            res_y: coordinates Y of target in meter
            res_y: coordinates Z of target in meter
    """
    ress = []
    check_inputs(points)
    xs, ys, zs, _, _, _ = points.T
    if len(points) == 1:
        x, y, z, d, a, i = points[0]
        range_x = d
        range_y = d
        range_z = d
    else:
        range_x = numpy.max(xs) - numpy.min(xs)
        range_y = numpy.max(ys) - numpy.min(ys)
        range_z = numpy.max(zs) - numpy.min(zs)
    mean_x = numpy.mean(xs)
    mean_y = numpy.mean(ys)
    mean_z = numpy.mean(zs)
    lx = numpy.linspace(-1, 1, n)
    ly = numpy.linspace(-1, 1, n)
    lz = numpy.linspace(-1, 1, n)
    min_score = sys.maxsize
    for ratio_x, ratio_y, ratio_z in itertools.product(lx, ly, lz):
        init = numpy.array([
            mean_x + ratio_x * range_x * 0.51,
            mean_y + ratio_y * range_y * 0.51,
            mean_z + ratio_z * range_z * 0.51,
        ])
        # print(f"{init = }")
        minimisation = scipy_optimize_minimize(
            get_score,
            init,
            points,
            method="L-BFGS-B",
            tol=0,
            options={
                "gtol": 0,
                "itol": 0,
            }
        )
        res = minimisation.x
        score = get_score(res, points)
        if score <= min_score:
            min_score = score
            result_point = res
    return result_point


def get_score(p: TYPE_RES, points: TYPE_POINTS) -> float:
    """
    Calcul score between the result p and input points.
    This function is the model that provide a score between p and points
    :param p: result as [x, y, z]
        x: coordinates X of target in meter
        y: coordinates Y of target in meter
        z: coordinates Z of target in meter
    :param points: array of points [x, y, z, d, a, i]
        x: Coordinate X in meter of the input point
        y: Coordinate Y in meter of the input point
        z (opt): Coordinate Z in meter of the input point, None if unknow
        d (opt): Distance from input point to the target in meter, None if unknow
        a (opt): Azimuth from input point to the target in degree, None if unknow
        i (opt): Inclinaison (vertical angle) from input point to the target in degree, None if unknow
    :return: score: A value to minimize that increase with the error of p
    """
    score = sum(get_list_scores(p, points))
    return score


def get_list_scores(p: TYPE_RES, points: TYPE_POINTS) -> list[float]:
    """
    List of individual score of each point
    :param p: result as [x, y, z]
        x: coordinates X of target in meter
        y: coordinates Y of target in meter
        z: coordinates Z of target in meter
    :param points: array of points [x, y, z, d, a, i]
        x: Coordinate X in meter of the input point
        y: Coordinate Y in meter of the input point
        z (opt): Coordinate Z in meter of the input point, None if unknow
        d (opt): Distance from input point to the target in meter, None if unknow
        a (opt): Azimuth from input point to the target in degree, None if unknow
        i (opt): Inclinaison (vertical angle) from input point to the target in degree, None if unknow
    :return: scores: A list of indiviual score for each input points
    """
    scores = [get_score_point(p, point) for point in points]
    return scores


def get_score_point(p: TYPE_RES, point: TYPE_POINT) -> float:
    """
    Calcul the score for a single point.
    :param p: result as [x, y, z]
        x: coordinates X of target in meter
        y: coordinates Y of target in meter
        z: coordinates Z of target in meter
    :param point: Fixed size list of values [x, y, z, d, a, i]
        x: Coordinate X in meter of the input point
        y: Coordinate Y in meter of the input point
        z (opt): Coordinate Z in meter of the input point, None if unknow
        d (opt): Distance from input point to the target in meter, None if unknow
        a (opt): Azimuth from input point to the target in degree, None if unknow
        i (opt): Inclinaison (vertical angle) from input point to the target in degree, None if unknow
    :return: score: indiviual score of the point
    """
    score = 0
    score_point = get_scores_point(p, point)
    for val in score_point.values():
        score += val
    # print(f"{score = }")
    return score


def get_scores_point(p: TYPE_RES, point: TYPE_POINT) -> dict[str, float]:
    """
    Calcul the score for a single point on 3 possibles errors: inclinaison, distance and azimuth.
    :param p: result as [x, y, z]
        x: coordinates X of target in meter
        y: coordinates Y of target in meter
        z: coordinates Z of target in meter
    :param point: Fixed size list of values [x, y, z, d, a, i]
        x: Coordinate X in meter of the input point
        y: Coordinate Y in meter of the input point
        z (opt): Coordinate Z in meter of the input point, None if unknow
        d (opt): Distance from input point to the target in meter, None if unknow
        a (opt): Azimuth from input point to the target in degree, None if unknow
        i (opt): Inclinaison (vertical angle) from input point to the target in degree, None if unknow
    :return: scores: Dictionnary of scores for maximum 3 measures: inclinaison, distance and azimuth
    """
    scores = {}
    errors, attributes = get_point_errors(p, point)
    # print("_" * 50)
    # print(f"{point = }")
    # print(f"{p = }")
    # print(f"{attributes = }")
    # print(f"{errors = }")
    if "inclinaison" in errors:
        scores["inclinaison"] = errors["inclinaison"]**2
    if "distance" in errors:
        scores["distance"] = errors["distance"]**2
    if "azimuth" in errors:
        scores["azimuth"] = (errors["azimuth"])**2
    if attributes["distance"] < 1:
        for score, val in scores.items():
            scores[score] = val / attributes["distance"]
    # print(f"{scores = }")
    return scores


def get_point_errors(p: TYPE_RES, point: TYPE_POINT) -> tuple[dict[str, float], dict[str, float]]:
    """
    Calcul the error for a single point on 3 possibles measures: inclinaison, distance and azimuth
    :param p: result as [x, y, z]
        x: coordinates X of target in meter
        y: coordinates Y of target in meter
        z: coordinates Z of target in meter
    :param point: Fixed size list of values [x, y, z, d, a, i]
        x: Coordinate X in meter of the input point
        y: Coordinate Y in meter of the input point
        z (opt): Coordinate Z in meter of the input point, None if unknow
        d (opt): Distance from input point to the target in meter, None if unknow
        a (opt): Azimuth from input point to the target in degree, None if unknow
        i (opt): Inclinaison (vertical angle) from input point to the target in degree, None if unknow
    :return: errors, attributes
        errors: Dictionnary of scores for maximum 3 measures: inclinaison, distance and azimuth
        attributes: Dictionnary of theorical values of measures between input point and target
    """
    x, y, z, d, a, i = point
    errors = {}
    has_d = d is not None and not math.isinf(d)
    has_a = a is not None and not math.isinf(a)
    has_i = i is not None and not math.isinf(i)
    attributes = get_point_attributes(p, x, y, z)
    if has_i:
        errors["inclinaison"] = attributes["inclinaison"] - i
    if has_d:
        errors["distance"] = attributes["distance"] - d
    if has_a:
        errors["azimuth"] = attributes["azimuth"] - a
    return errors, attributes
    
    
def get_point_attributes(p: TYPE_RES, x: float, y: float, z: float) -> dict[str, float]:
    """
    Calcul
    :param p: result as [x, y, z]
        x: coordinates X of target in meter
        y: coordinates Y of target in meter
        z: coordinates Z of target in meter
    :param x: Coordinates X of input point in meter
    :param y: Coordinates Y of input point in meter
    :param z: Coordinates Z of input point in meter
    :return: attributes: Dictionnary of theorical values of measures between input point and target
    """
    return {
        "distance": utils.distance([x, y, z], p),
        "azimuth": utils.azimuth(source=[x, y, z], target=p),
        "inclinaison": utils.inclinaison(source=[x, y, z], target=p),
    }


def display(points, result_point, eps=10e-2):
    gxr, gyr, zr = result_point
    for i, point in enumerate(points):
        gx, gy, z, d, azim, incl = point
        plt.plot([gx, gxr], [gy, gyr])
        plt.scatter([gx], [gy], color="red")
        txt = f"Point {i+1} ({gx}, {gy}, {z})\n"
        if d is not None:
            txt += f"Dist={round(d, 1)}\n"
        if azim is not None:
            txt += f"Azimuth={round(azim, 1)}\n"
        if incl is not None:
            txt += f"Inclinaison={round(incl, 1)}\n"
        errors, attributes = get_point_errors(result_point, point)
        for error_name, error_value in errors.items():
            if error_value < eps:
                continue
            txt += f"Error {error_name}={round(error_value, 2)}\n"
        plt.annotate(txt, (gx, gy))
    plt.scatter([gxr], [gyr], color="green")
    plt.annotate(f"Result:\n  X={round(gxr, 1)}\n  Y={round(gyr, 1)}\n  Z={round(zr, 1)}m", (gxr, gyr))
    plt.show()


def check_inputs(points: TYPE_POINTS) -> None:
    nb_var_total = 0
    for iter_i, point in enumerate(points):
        nb_var = 0
        x, y, z, d, a, i = point
        if x is None:
            raise Exception(f"Point {iter_i} : Coordinate X cannot be None")
        if y is None:
            raise Exception(f"Point {iter_i} : Coordinate Y cannot be None")
        if z is None:
            raise Exception(f"Point {iter_i} : Coordinate Z cannot be None, enter 0 insteed")
        if d is not None:
            nb_var += 1
            if d < 0:
                raise Exception(f"Point {iter_i} : Negative distance: {d = }")
        if a is not None:
            nb_var += 2
            if a < 0 or a > 360:
                raise Exception(f"Point {iter_i} : Azimuth over 0 and inferior to 360")
        if i is not None:
            nb_var += 1
            if i < -90 or i > 90:
                raise Exception(f"Point {iter_i} : Inclinaison over -90 and inferior to 90")
        if nb_var == 0:
            raise Exception(f"Point {iter_i} : No measure to target entered")
        nb_var_total += nb_var
    # if nb_var_total < 3:
    #     raise Exception(f"Not enough measures: {nb_var_total = }")
