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
    # 最大需要的资源数
    max_need = [0, 0, 0]
    # 已经分配的资源数
    allocation = [0, 0, 0]
    # 仍然需要的资源数
    still_need = []
    # 资源目录
    resource_dictionary = Resource_dictionary().table
    # 特殊事件
    event = None
    # 特殊资源列表 第一项是缓冲区 第二项是进程
    special_resource = []
    # 是否在使用缓冲区的标志位
    use_buffer = 0
    # 要发送的信息
    message_send = []
    # 接收到的信息
    message_receive = []
    # 读取到的文件的内容
    file_read = []
    # 要访问的文件
    file_access = []
    # 该进程拥有的线程列表
    thread_table = []
    # 线程创建列表
    thread_create_list = []
    # 父进程
    main_process = None
    # 是否是线程 标志位
    thread_flag = 0
    # 分配到的内存编号
    memory_number = None
    # 进程中内存的使用情况
    memory_use_in_process = {}
    # 页表
    page_table = []
    # 页面的数量
    page_number = None
    # 页面的访问列表
    page_access_list = []
    # 内存中的页面数量
    page_in_memory_number = 0
    # 页面栈(用来查找最先进入内存的页面)
    page_stack = []
    # 优先级
    priority = None
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
    4 进程通信测试
    5 外存访问测试
    6 线程测试
    '''

    def __init__(self, name, work_time, priority, resource, event, special_resource, thread_flag):
        self.PCB = copy.deepcopy(self.PCB)
        self.PCB['name'] = name
        self.PCB['work_time'] = work_time
        self.PCB['total_work_time'] = work_time
        self.priority = priority
        self.PCB['priority'] = priority
        self.PCB['state'] = 0

        self.PCB['resource'] = resource
        self.max_need = copy.deepcopy(self.max_need)
        self.still_need = copy.deepcopy(self.still_need)
        self.allocation = copy.deepcopy(self.allocation)
        self.event = copy.deepcopy(self.event)
        self.special_resource = copy.deepcopy(self.special_resource)
        self.message_send = copy.deepcopy(self.message_receive)
        self.message_receive = copy.deepcopy(self.message_receive)
        self.file_access = copy.deepcopy(self.file_access)
        self.file_read = copy.deepcopy(self.file_read)
        self.thread_table = copy.deepcopy(self.thread_table)
        self.thread_create_list = copy.deepcopy(self.thread_create_list)
        self.page_table = copy.deepcopy(self.page_table)
        self.page_access_list = copy.deepcopy(self.page_access_list)
        self.memory_use_in_process = copy.deepcopy(self.memory_use_in_process)
        self.page_stack = copy.deepcopy(self.page_stack)
        self.event = event
        self.special_resource = special_resource
        self.thread_flag = thread_flag
        for single_time_resource in resource:
            for i in range(len(resource[single_time_resource])):
                self.max_need[i] += resource[single_time_resource][i]
                # self.max_need[self.resource_dictionary[single_time_resource]] += 1
        self.still_need = self.max_need
        # for i in range(len(self.max_need)):
        #     self.still_need[i] = self.max_need[i] - self.allocation[i]

    def __lt__(self, other):
        return self.priority < other.priority

    def set_message(self, message):
        self.message_send = message

    def get_message(self):
        return self.message_receive

    def set_file_access(self, file):
        self.file_access = file

    def get_file_content(self):
        return self.file_read

    def set_thread_create_table(self, thread_create_list):
        self.thread_create_list = thread_create_list

    def set_page_table(self, page_table):
        self.page_table = page_table

    def set_page_access_list(self, page_access_list, page_number):
        self.page_access_list = page_access_list
        self.page_number = page_number
