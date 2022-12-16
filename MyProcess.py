# -*- coding: utf-8 -*-
"""
@author yumu
@className Process
@version 1.0.0
@describe TODO
"""
from Resource import *
import copy
class MyProcess:
    PCB = {}
    max_need = [0,0,0]
    allocation = [0,0,0]
    still_need = []
    resource_dictionary = Resource_dictionary().table
    event = None
    special_resource = []
    use_buffer = 0
    '''
    进程类，用于创建进程
    在创建一个进程的时候（实例化一个进程对象），需要给出进程的名字，工作所需时间，优先级
    进程状态对应关系如下
    0 创建态
    1 就绪态
    2 运行态
    3 阻塞态
    4 终止态
    
    事件对应关系如下
    0 无特殊事件
    1 生产
    2 消费
    3 进程同步测试
    
    '''

    def __init__(self,name,work_time,priority,resource,event,special_resource):
        self.PCB = copy.deepcopy(self.PCB)
        self.PCB['name'] = name
        self.PCB['work_time'] = work_time
        self.PCB['total_work_time'] = work_time
        self.PCB['priority'] = priority
        self.PCB['state'] = 0

        self.PCB['resource'] = resource
        self.max_need = copy.deepcopy(self.max_need)
        self.still_need = copy.deepcopy(self.still_need)
        self.allocation = copy.deepcopy(self.allocation)
        self.event = event
        self.special_resource = special_resource
        for single_time_resource in resource:
            for i in range(len(resource[single_time_resource])):
                self.max_need[i] += resource[single_time_resource][i]
                # self.max_need[self.resource_dictionary[single_time_resource]] += 1
        self.still_need = self.max_need
        # for i in range(len(self.max_need)):
        #     self.still_need[i] = self.max_need[i] - self.allocation[i]

    def __lt__(self, other):
        return self.PCB['priority'] < other.PCB['priority']