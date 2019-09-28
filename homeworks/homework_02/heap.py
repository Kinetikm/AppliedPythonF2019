#!/usr/bin/env python
# coding: utf-8


class Heap(object):

    def __init__(self, array):
        self.heap = array[:]
        self.build_heap()

    def sift_down(self, i):
        left = 2 * i + 1
        right = 2 * i + 2
        largest = i
        if (left < len(self.heap)) \
                and comparator_d(self.heap[left], self.heap[largest]):
            largest = left
        if (right < len(self.heap)) \
                and comparator_d(self.heap[right], self.heap[largest]):
            largest = right
        if largest != i:
            self.heap[i], self.heap[largest] = self.heap[largest], self.heap[i]
            self.sift_down(largest)

    def add(self, elem_with_priority):
        self.heap.append(elem_with_priority)
        self.build_heap()

    def build_heap(self):
        length = len(self.heap) // 2
        for i in range(length, -1, -1):
            self.sift_down(i)


class MaxHeap(Heap):

    def __init__(self, array):
        super().__init__(array)

    def extract_maximum(self):
        result = self.heap.pop(0)
        self.build_heap()
        return result


def comparator_d(x, y):
    if x[0] == y[0]:
        return x[1] >= y[1]
    elif x[0] > y[0]:
        return True
    else:
        return False
