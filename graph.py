import math


EARTH_RADIUS_KM = 6371.0


def calculate_distance(city1, city2):
    lat1 = math.radians(city1.latitude)
    lon1 = math.radians(city1.longitude)

    lat2 = math.radians(city2.latitude)
    lon2 = math.radians(city2.longitude)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return EARTH_RADIUS_KM * c


def build_distance_matrix(cities):
    n = len(cities)

    matrix = [
        [0.0] * n
        for _ in range(n)
    ]

    for i in range(n):
        for j in range(i + 1, n):
            distance = calculate_distance(
                cities[i],
                cities[j]
            )

            matrix[i][j] = distance
            matrix[j][i] = distance

    return matrix


def get_distance(
    matrix,
    city1_id,
    city2_id
):
    return matrix[city1_id][city2_id]


def calculate_route_distance(
    route,
    matrix
):
    if len(route) < 2:
        return 0.0

    total = 0.0

    for i in range(len(route) - 1):
        total += matrix[
            route[i]
        ][
            route[i + 1]
        ]

    return total


def calculate_closed_route_distance(
    route,
    matrix
):
    if len(route) < 2:
        return 0.0

    total = calculate_route_distance(
        route,
        matrix
    )

    if route[0] != route[-1]:
        total += matrix[
            route[-1]
        ][
            route[0]
        ]

    return total