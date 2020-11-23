import csv
import random as r
from math import exp
import matplotlib.pyplot as plt

path = "C:/Users/pauer/Desktop"
# Defining the zones
zone_1 = {"mx": 150,
          "my": 150,
          "dx": r.randint(60, 90),
          "dy": r.randint(60, 90)}

zone_2 = {"mx": 150,
          "my": -150,
          "dx": r.randint(60, 90),
          "dy": r.randint(60, 90)}

zone_3 = {"mx": -150,
          "my": -150,
          "dx": r.randint(60, 90),
          "dy": r.randint(60, 90)}


list_zone = []
list_x = []
list_y = []


def choose_zone():
    return r.randint(1, 3)


def get_point(zone, axis):
    threshold = r.random()
    g = 0.0
    while threshold > g:
        point = r.randint(-300, 300)
        g = gauss(zone, axis, point)
    return point


def gauss(zone, axis, nr):
    if zone == 1:
        m, d = zone_1[f"m{axis}"], zone_1[f"d{axis}"]
    elif zone == 2:
        m, d = zone_2[f"m{axis}"], zone_2[f"d{axis}"]
    else:
        m, d = zone_3[f"m{axis}"], zone_3[f"d{axis}"]
    return exp(-(((m-nr)**2)/(2*d**2)))


def plot(x_axis, y_axis):
    plt.grid(color="gray")
    plt.scatter(x_axis, y_axis, s=1, color="red", zorder=2)
    plt.savefig(f"{path}/graph.png")
    plt.show()


def write_file(zones, x_axis, y_axis):
    with open(f"{path}/points.csv", "w+", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        [writer.writerow([f"{zones[_]}", f"{x_axis[_]}", f"{y_axis[_]}"]) for _ in range(3000)]


for _ in range(3000):
    zone = choose_zone()
    list_zone.append(zone)
    x = get_point(zone, "x")
    list_x.append(x)
    y = get_point(zone, "y")
    list_y.append(y)

write_file(list_zone, list_x, list_y)
plot(list_x, list_y)
