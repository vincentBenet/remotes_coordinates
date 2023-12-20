import numpy
import remotes_coordinates


if __name__ == "__main__":
    import os
    path = os.path.join(os.path.dirname(__file__), "data_test.gpkg")
    xs, ys, zs, distances, azimuths, inclinaisons = remotes_coordinates.load_file(path)
    print(f"{xs = }")
    print(f"{ys = }")
    print(f"{zs = }")
    print(f"{distances = }")
    print(f"{azimuths = }")
    print(f"{inclinaisons = }")
    points = numpy.array([xs, ys, zs, distances, azimuths, inclinaisons]).T
    x, y, z = remotes_coordinates.calcul(points)
    print(f"{x = }")
    print(f"{y = }")
    print(f"{z = }")

    xa = 310570
    ya = 5646809

    x_error = abs(x-xa)
    y_error = abs(y-ya)
    print(f"{x_error = }")
    print(f"{y_error = }")
