#!/usr/bin/env python3

def edge_map(edges):
    """edges should be dels or adds and therefore node-id disjoint, except at junctions."""
    m = {}
    for e in edges:
        a, b = e
        if a not in m:
            m[a] = []
        m[a].append(b)
        if len(m[a]) > 1:
            assert(len(m[a]) == 2)
        if b not in m:
            m[b] = []
        m[b].append(a)
        if len(m[b]) > 1:
            assert(len(m[b]) == 2)
    return m

