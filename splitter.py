#!/usr/bin/env python3

# Compares 2 local optima, and splits the k-move describing the difference between the 2 local optima into segments.

import tour_util
from edge_bank import EdgeBank

class Splitter:
    """Takes 2 tours, and returns k-move segments.
    If there are no junctions, then splitting simply becomes the task of identifying disjoint sets of edges.
    """
    def __init__(self, old_tour, new_tour):
        common, dels, adds = tour_util.factor(old_tour, new_tour)
        assert(len(dels) == len(adds))
        self.edge_bank = EdgeBank(dels, adds)
        self.segment_start = None # start id of current segment.
        self.segment_end = None # end id of current segment.
        self.dels = [] # dels in the current segment.
        self.adds = [] # adds in the current segment.

    def get_segments(self):
        segments = [self.walk()]
        while segments[-1] is not None:
            segments.append(self.walk())
        segments.pop()
        return segments

    def step_add(self):
        if len(self.dels) == 0:
            start = self.segment_start
        else:
            start = self.dels[-1][-1]
        edge = self.edge_bank.pop_add(start)
        self.adds.append(edge)
        self.segment_end = edge[-1]

    def step_del(self):
        if len(self.adds) == 0:
            start = self.segment_start
        else:
            start = self.adds[-1][-1]
        edge = self.edge_bank.pop_del(start)
        self.dels.append(edge)
        self.segment_end = edge[-1]

    def pop_segment(self):
        """Resets current segment, returning current segment as dict."""
        segment = {
                'start': self.segment_start,
                'end': self.segment_end,
                'dels': self.dels[:],
                'adds': self.adds[:],
        }
        self.segment_start = None
        self.segment_end = None
        self.dels = []
        self.adds = []
        return segment

    def walk(self):
        """Attempts to return a random segment."""
        if len(self.edge_bank.junctions) > 0:
            self.segment_start = next(iter(self.edge_bank.junctions))
            while not self.edge_bank.has_node(self.segment_start):
                self.edge_bank.junctions.remove(self.segment_start)
                if len(self.edge_bank.junctions) == 0:
                    self.segment_start = self.edge_bank.random_start()
                    if self.segment_start is None:
                        return None
                    break
                self.segment_start = next(iter(self.edge_bank.junctions))
        else:
            self.segment_start = self.edge_bank.random_start()
            if self.segment_start is None:
                return None
        while self.step():
            pass
        # We should have a segment now.
        return self.pop_segment()

    def step(self):
        """Performs a step based on current state. Returns true if should continue, false if not."""
        assert(abs(len(self.dels) - len(self.adds)) < 2)
        if len(self.dels) < len(self.adds):
            self.step_del()
        elif len(self.adds) < len(self.dels):
            self.step_add()
        elif len(self.adds) == 0:
            if self.edge_bank.has_add(self.segment_start):
                self.step_add()
            else:
                self.step_del()
        else:
            if self.edge_bank.has_add(self.dels[-1][-1]):
                self.step_add()
            else:
                self.step_del()
        return self.segment_end not in self.edge_bank.junctions and self.segment_end != self.segment_start

