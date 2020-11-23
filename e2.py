import random as r
import csv
import matplotlib.pyplot as plt

path = "C:/Users/pauer/Desktop"
center_colors = ["red", "blue", "green", "orange", "yellow", "purple", "black", "gray", "brown", "pink"]


def select_read_points(center_of_classes, classes=True):
    random_numbers = [r.randint(0, 2999) for _ in range(center_of_classes) if classes]
    points_list = []
    index = 0
    with open(f"{path}/points.csv", "r") as csv_file:
        reader = csv.reader(csv_file, delimiter=",")
        if classes:
            for line in reader:
                if index in random_numbers:
                    points_list.append((line[1], line[2]))
                index += 1
        else:
            points_list = [(line[1], line[2]) for line in reader]
    return points_list


def calculate_similarity(center_points, all_points):
    for point in all_points:
        max_dissimilarity = 1000
        dissimilarity_index = 0
        x_point, y_point = int(point[0]), int(point[1])
        for center_point in center_points:
            dissimilarity = abs(x_point - int(center_point[0])) + abs(y_point - int(center_point[1]))
            if dissimilarity < max_dissimilarity:
                max_dissimilarity, dissimilarity_index = dissimilarity, center_points.index(center_point)
        points_per_center[dissimilarity_index].append(point)


def plot(points_per_center):
    index = 0
    for group in points_per_center:
        x_axis, y_axis = [], []
        for x, y in group:
            x_axis.append(int(x)), y_axis.append(int(y))
        plt.scatter(x_axis, y_axis, s=0.3, color=center_colors[index])
        index += 1
    plt.grid(color="gray")
    plt.savefig(f"{path}/graph_2.png")
    plt.show()


center_of_classes = r.randint(2, 10)
center_points = select_read_points(center_of_classes)
all_points = select_read_points(center_of_classes, False)
points_per_center = [[] for _ in range(len(center_points))]
calculate_similarity(center_points, all_points)
plot(points_per_center)
