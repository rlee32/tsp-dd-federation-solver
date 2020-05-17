#/usr/bin/env python3

import tour_util
import basic

def swap(tour, i, j):
    """Performs a sequential 2-opt swap on a tour."""
    new_tour = tour[:i+1] + tour[j:i:-1] + tour[j+1:]
    assert(len(tour) == len(new_tour))
    return new_tour

def improve(xy, tour):
    n = len(tour)
    for i in range(n):
        ilen = basic.distance(xy, tour[i], tour[(i+1)%n])
        for j in range(i + 2, n):
            jlen = basic.distance(xy, tour[j], tour[(j+1)%n])
            cost = basic.distance(xy, tour[i], tour[j]) + basic.distance(xy, tour[(i+1)%n], tour[(j+1)%n])
            improvement = ilen + jlen - cost
            if improvement > 0:
                new_tour = swap(tour, i, j)
                assert(tour != new_tour)
                return new_tour, improvement
    return tour, 0

def optimize(xy, tour):
    new_tour, improvement = improve(xy, tour)
    total_improvement = improvement
    while improvement > 0:
        new_tour, improvement = improve(xy, new_tour)
        total_improvement += improvement
    new_length = tour_util.length(xy, new_tour)
    print('optimized length: {}'.format(new_length))
    return new_tour, new_length
