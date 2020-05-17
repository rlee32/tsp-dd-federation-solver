#!/usr/bin/env python3

import edge_map

class EdgeBank:
    def __init__(self, dels, adds):
        self.delmap = edge_map.edge_map(dels)
        self.addmap = edge_map.edge_map(adds)
        self.junctions = set()
        for key in self.delmap:
            n = len(self.delmap[key])
            assert(n == 1 or n == 2)
            if n == 2:
                self.junctions.add(key)
        for key in self.addmap:
            n = len(self.addmap[key])
            assert(n == 1 or n == 2)
            if n == 2:
                self.junctions.add(key)

    def pop_add(self, start):
        """Pops an arbitrary addition edge off of the internal map containing the given start."""
        end = self.addmap[start].pop()
        if len(self.addmap[start]) == 0:
            del self.addmap[start]
        self.addmap[end].remove(start)
        if len(self.addmap[end]) == 0:
            del self.addmap[end]
        return (start, end)

    def pop_del(self, start):
        """Pops an arbitrary deletion edge off of the internal map containing the given start."""
        end = self.delmap[start].pop()
        if len(self.delmap[start]) == 0:
            del self.delmap[start]
        self.delmap[end].remove(start)
        if len(self.delmap[end]) == 0:
            del self.delmap[end]
        return (start, end)

    def random_start(self):
        """Returns an arbitrary start id off of the internal addition edge map.
        Used to initialize a walk.
        """
        for key in self.addmap:
            return key
        for key in self.delmap:
            return key

    def has_add(self, i):
        return i in self.addmap

    def has_del(self, i):
        return i in self.delmap

    def has_node(self, i):
        return self.has_add(i) or self.has_del(i)
