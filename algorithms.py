import itertools
import math
import time


def tour_length(route, matrix):
    if len(route) < 2:
        return 0.0

    return sum(
        matrix[
            route[i]
        ][
            route[(i + 1) % len(route)]
        ]
        for i in range(len(route))
    )


def solve_brute_force(matrix, start=0):
    n = len(matrix)

    if n == 0:
        return [], 0.0, 0

    if n == 1:
        return [start], 0.0, 1

    remaining = [
        city
        for city in range(n)
        if city != start
    ]

    best_route = None
    best_distance = math.inf
    checked = 0

    for permutation in itertools.permutations(remaining):
        route = [start] + list(permutation)
        distance = tour_length(
            route,
            matrix
        )

        checked += 1

        if distance < best_distance:
            best_distance = distance
            best_route = route

    return best_route, best_distance, checked


def solve_held_karp(matrix, start=0):
    n = len(matrix)

    if n == 0:
        return [], 0.0

    if n == 1:
        return [start], 0.0

    cities = [
        city
        for city in range(n)
        if city != start
    ]

    index = {
        city: i
        for i, city in enumerate(cities)
    }

    dp = {}
    parent = {}

    for city in cities:
        mask = 1 << index[city]
        dp[(mask, city)] = matrix[start][city]
        parent[(mask, city)] = start

    for size in range(2, len(cities) + 1):
        for subset in itertools.combinations(
            cities,
            size
        ):
            mask = 0

            for city in subset:
                mask |= 1 << index[city]

            for current in subset:
                current_bit = 1 << index[current]
                previous_mask = mask ^ current_bit

                best = math.inf
                best_previous = None

                for previous in subset:
                    if previous == current:
                        continue

                    value = (
                        dp[
                            (previous_mask, previous)
                        ]
                        + matrix[previous][current]
                    )

                    if value < best:
                        best = value
                        best_previous = previous

                dp[(mask, current)] = best
                parent[(mask, current)] = best_previous

    full_mask = (1 << len(cities)) - 1

    best_distance = math.inf
    best_last = None

    for city in cities:
        value = (
            dp[(full_mask, city)]
            + matrix[city][start]
        )

        if value < best_distance:
            best_distance = value
            best_last = city

    route = []
    mask = full_mask
    current = best_last

    while current != start:
        route.append(current)

        previous = parent[
            (mask, current)
        ]

        mask ^= 1 << index[current]
        current = previous

    route.reverse()

    return [start] + route, best_distance


def solve_nearest_neighbor(matrix, start=0):
    n = len(matrix)

    if n == 0:
        return [], 0.0

    if n == 1:
        return [start], 0.0

    visited = [False] * n
    visited[start] = True

    route = [start]
    current = start

    for _ in range(n - 1):
        nearest = None
        nearest_distance = math.inf

        for city in range(n):
            if not visited[city]:
                distance = matrix[current][city]

                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest = city

        route.append(nearest)
        visited[nearest] = True
        current = nearest

    return route, tour_length(route, matrix)


def two_opt(route, matrix):
    if len(route) < 4:
        return route[:], tour_length(
            route,
            matrix
        )

    best = route[:]
    improved = True

    while improved:
        improved = False
        best_distance = tour_length(
            best,
            matrix
        )

        n = len(best)

        for i in range(1, n - 2):
            for j in range(i + 1, n - 1):
                candidate = (
                    best[:i]
                    + best[i:j + 1][::-1]
                    + best[j + 1:]
                )

                candidate_distance = tour_length(
                    candidate,
                    matrix
                )

                if candidate_distance < best_distance:
                    best = candidate
                    best_distance = candidate_distance
                    improved = True
                    break

            if improved:
                break

    return best, tour_length(
        best,
        matrix
    )


def solve_heuristic(matrix, start=0):
    route, _ = solve_nearest_neighbor(
        matrix,
        start
    )

    return two_opt(
        route,
        matrix
    )


def run_algorithm(
    algorithm_name,
    matrix,
    start=0
):
    start_time = time.perf_counter()

    if algorithm_name == "Vét cạn":
        route, distance, checked = solve_brute_force(
            matrix,
            start
        )

        info = {
            "algorithm": "Vét cạn",
            "complexity": "O(n!)",
            "checked": checked
        }

    elif algorithm_name == "Quy hoạch động":
        route, distance = solve_held_karp(
            matrix,
            start
        )

        info = {
            "algorithm": "Quy hoạch động (Held-Karp)",
            "complexity": "O(n² × 2ⁿ)"
        }

    elif algorithm_name == "Heuristic":
        route, distance = solve_heuristic(
            matrix,
            start
        )

        info = {
            "algorithm": "Heuristic (Nearest Neighbor + 2-opt)",
            "complexity": "O(n²)"
        }

    else:
        raise ValueError(
            "Thuật toán không hợp lệ."
        )

    execution_time = (
        time.perf_counter()
        - start_time
    )

    return {
        "algorithm": algorithm_name,
        "route": route,
        "distance": distance,
        "execution_time": execution_time,
        "processing_info": info
    }