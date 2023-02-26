# -*- coding: utf-8 -*-
"""
@author yumu
@className Resource
@version 1.0.0
@describe TODO
"""
import queue


class Resource:
    name = None
    block_process_queue = queue.Queue()
    number = None

    def __init__(self, name, number):
        self.number = number
        self.name = name


class Resource_allocation:
    resource_allocation_log = []
    resource_allocation_table = {}
    available = []
    safety_sequence = []


class Resource_dictionary:
    table = {
        "A": 0,
        "B": 1,
        "C": 2,
    }


class Event:
    event_dic = {

    }
