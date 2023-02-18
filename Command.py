# -*- coding: utf-8 -*-
"""
@author yumu
@className Command
@version 1.0.0
@describe TODO
"""
import copy
import queue

from MyOS import *


class Command:
    # 输出cpu日志
    def print_cpu_log(self, os: MyOS):
        print(os.cpu.cpu_log)

    # 输出目前的进程队列
    def print_process_queue(self, os: MyOS):
        for info in os.print_process_queue:
            print(info)

    # 输出目前的系统时间
    def print_os_time(self, os: MyOS):
        print("当前系统时间为:" + str(os.os_time))

    # 输出系统资源分配记录
    def print_resource_allocation_log(self, os: MyOS):
        print(os.resource_allocation.resource_allocation_log)

    # 输出进程收到的信息
    def print_process_receive_message(self, os: MyOS):
        for process in os.process_table:
            print("进程" + process.PCB['name'] + "收到的消息列表为" + str(process.message_receive))

    # 输出进程访问外存读取到的内容
    def print_process_read_file_content(self, os: MyOS):
        for process in os.process_table:
            print("进程" + process.PCB['name'] + "读取到的文件内容是" + str(process.file_read))

    # 挂起
    def suspend(self, os: MyOS, process_name: str):
        suspend_process = None
        for process in os.process_table:
            if process_name == process.PCB['name']:
                suspend_process = process
                break
        if suspend_process.PCB['state'] == 2:
            os.cpu.flag = 1
            os.cpu.process_in_cpu = None
            suspend_process.PCB['state'] = 1
            os.suspend_process_queue.append(suspend_process)

        elif suspend_process.PCB['state'] == 1:
            q = queue.PriorityQueue()
            while not os.process_queue.empty():
                temp_process = os.process_queue.get()
                if temp_process.PCB['name'] == process_name:
                    os.suspend_process_queue.append(temp_process)
                else:
                    q.put(temp_process)
            while not q.empty():
                os.process_queue.put(q.get())

        elif suspend_process.PCB['state'] == 3:
            os.suspend_process_queue.append(suspend_process)
            if suspend_process in os.block_process_queue:
                os.block_process_queue.remove(suspend_process)

    # 唤醒
    def activation(self, os: MyOS, process_name: str):
        activation_process = None
        for process in os.process_table:
            if process_name == process.PCB['name']:
                activation_process = process
                break
        if activation_process.PCB['state'] == 1:
            os.process_queue.put(activation_process)
            if activation_process in os.suspend_process_queue:
                os.suspend_process_queue.remove(activation_process)

        elif activation_process.PCB['state'] == 3:
            os.block_process_queue.append(activation_process)
            if activation_process in os.suspend_process_queue:
                os.suspend_process_queue.remove(activation_process)

    # 输出内存使用情况
    def print_memory_use(self, os: MyOS):
        print("内存使用情况如下")
        print("分区号", "大小（KB）", "起始地址（K）", "状态", "分配给的进程")
        for memory_use in os.memory_use_table:
            print(str(memory_use[0]), str(memory_use[1]), str(memory_use[2]), end=" ")
            if memory_use[3] == 0:
                print("未分配", end=" ")
            elif memory_use[3] == 1:
                print("已分配", end=" ")
            if memory_use[4] == None:
                print("无")
            else:
                print(memory_use[4].PCB['name'])

    # 输出页表
    def print_page_table(self, os: MyOS):
        for process in os.process_table:
            print("进程" + process.PCB['name'] + "页表如下")
            print("页号", "内存块号", "状态位", "访问字段", "修改位", "外存地址")
            for index in range(len(process.page_table)):
                print(str(index), process.page_table[index])

    # 输出页表调入和换入换出记录
    def print_page_access_log(self, os: MyOS):
        print(os.page_access_log)

    def print_buffer(self, os: MyOS):
        print("缓冲区如下")
        print(os.buffer)