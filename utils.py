# -*- coding: utf-8 -*-
"""
@author yumu
@className utils
@version 1.0.0
@describe TODO
"""
from MyProcess import *
from MyCPU import *
from MyOS import *
import random
from Command import *
# 基于时间片轮转法的进程互斥测试
def auto_process_mutual_exclusion_test(time_slice:int):
    p0 = MyProcess(name="p0", work_time=10, priority=1, resource={
        0: [0, 0, 0]
    },event=2,special_resource=[1,{}])
    p1 = MyProcess(name="p1", work_time=10, priority=1, resource={
        0: [0, 0, 0]
    },event=2,special_resource=[1,{}])
    p2 = MyProcess(name="p2", work_time=10, priority=1, resource={
        0: [0, 0, 0]
    },event=1,special_resource=[1,{}])
    p3 = MyProcess(name="p3", work_time=10, priority=1, resource={
        0: [0, 0, 0]
    },event=2,special_resource=[1,{}])
    p4 = MyProcess(name="p4", work_time=10, priority=1, resource={
        0: [0, 0, 0]
    },event=1,special_resource=[1,{}])
    processes = [p0, p1, p2, p3, p4]
    os = MyOS(processes=processes, process_scheduling_algorithm=0, available=[0,0,0], buffer_size= 5,time_slice=time_slice)
    # 另开一个线程来运行os
    os_thread = threading.Thread(target=os.run)
    os_thread.start()
    while True:
        command = Command()
        command.print_process_queue(os)
        print()
        time.sleep(2)

# 基于时间片轮转法的进程同步测试
def auto_process_synchronization_test():
    p0 = MyProcess(name="p0", work_time=10, priority=1, resource={
        0: [0, 0, 0]
    }, event=3, special_resource=[0, {3:"p1"}])
    p1 = MyProcess(name="p1", work_time=10, priority=1, resource={
        0: [0, 0, 0]
    }, event=3, special_resource=[0, {}])
# 时间片轮转法进程调度测试
def time_slice_rotation_test(time_slice:int,process_num:int)->MyOS:
    processes =[]
    # 随机生成n个进程进行运行
    for i in range(process_num):
        processes.append(MyProcess(name="p"+str(i),work_time=random.randint(1,10),priority=1))
    os = MyOS(processes=processes,process_scheduling_algorithm=0,time_slice=time_slice)
    # 另开一个线程来运行os
    os_thread = threading.Thread(target=os.run)
    os_thread.start()
    return os

# 非抢占式静态优先级调度测试
def static_priority_scheduling_test(process_num:int)->MyOS:
    processes = []
    # 随机生成n个进程进行运行
    for i in range(process_num):
        processes.append(MyProcess(name="p" + str(i), work_time=random.randint(1, 10), priority=random.randint(1, 10)))
    os = MyOS(processes=processes, process_scheduling_algorithm=1)
    # 另开一个线程来运行os
    os_thread = threading.Thread(target=os.run)
    os_thread.start()
    return os

# 基于时间片轮转法进程调度的死锁处理测试
def deadlock_handling_test(time_slice:int)->MyOS:
    p0 = MyProcess(name="p0",work_time=10,priority=1,resource={
        0:[0,1,0],
        3:[7,4,3]
    },event=0,special_resource=[0,{}])
    p1 = MyProcess(name="p1", work_time=10, priority=1, resource={
        0: [2, 0, 0],
        3: [1, 2, 2]
    },event=0,special_resource=[0,{}])
    p2 = MyProcess(name="p2", work_time=10, priority=1, resource={
        0: [3, 0, 2],
        3: [6, 0, 0]
    },event=0,special_resource=[0,{}])
    p3 = MyProcess(name="p3", work_time=10, priority=1, resource={
        0: [2, 1, 1],
        3: [0, 1, 1]
    },event=0,special_resource=[0,{}])
    p4 = MyProcess(name="p4", work_time=10, priority=1, resource={
        0: [0, 0, 2],
        3: [4, 3, 1]
    },event=0,special_resource=[0,{}])
    processes = [p0,p1,p2,p3,p4]
    os = MyOS(processes=processes, process_scheduling_algorithm=0, available=[10,5,7] ,time_slice=time_slice)
    # 另开一个线程来运行os
    os_thread = threading.Thread(target=os.run)
    os_thread.start()
    return os


