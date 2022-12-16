# -*- coding: utf-8 -*-
"""
@author yumu
@className pr
@version 1.0.0
@describe TODO
"""
import heapq

class MyPriorityQueue:
    def __init__(self):
        self.queue = []
        self.index = 0
    # 入队元素
    def put(self, item, priority):
        heapq.heappush(self.queue, (-priority, self.index, item))
        self.index += 1
    def get(self):
        return heapq.heappop(self.queue)[-1]

    def empty(self):
        if len(self.queue)==0:
            return True
        return False