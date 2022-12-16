# -*- coding: utf-8 -*-
"""
@author yumu
@className Command
@version 1.0.0
@describe TODO
"""
import copy

from MyOS import *
class Command:
    # 输出cpu日志
    def print_cpu_log(self,os:MyOS):
        print(os.cpu.cpu_log)

    # 输出目前的进程队列
    def print_process_queue(self,os:MyOS):
        for info in os.print_process_queue:
            print(info)
    # 输出目前的系统时间
    def print_os_time(self,os:MyOS):
        print("当前系统时间为:" + str(os.os_time))

    # 输出系统资源分配记录
    def print_resource_allocation_log(self,os:MyOS):
        print(os.resource_allocation.resource_allocation_log)