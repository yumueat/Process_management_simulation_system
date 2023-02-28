# -*- coding: utf-8 -*-
"""
@author yumu
@className utils
@version 1.0.0
@describe TODO 1 静态优先级测试 2 挂起 3 最坏边界值测试 4 梳理系统结构
"""
import threading

from MyProcess import *
from MyCPU import *
from MyOS import *
import random
from Command import *

# 时间片轮转法进程调度测试
def auto_time_slice_rotation_test(time_slice: int, process_num: int):
    processes = []
    # 随机生成n个进程进行运行
    for i in range(process_num):
        # 每个进程均采用最简单的配置，不额外设置需要的资源，特殊资源，特殊事件
        temp_process = MyProcess(name="p" + str(i), work_time=random.randint(1, 10), priority=1,resource=[],event=[],special_resource=[0,{}],thread_flag=0)
        # 不对进程需要的内存页面进行设置
        temp_process.set_page_access_list(page_access_list=[],page_number=0)
        processes.append(temp_process)
    os = MyOS(processes=processes, process_scheduling_algorithm=0, available=[0,0,0],buffer_size=5,memory_size=100,memory_number=10,time_slice=time_slice)
    # 另开一个线程来运行os
    os_thread = threading.Thread(target=os.run)
    os_thread.start()
    while True:
        command = Command()
        command.print_process_queue(os)
        print()
        time.sleep(2)


# 非抢占式静态优先级调度测试
def auto_static_priority_scheduling_test(process_num: int):
    processes = []
    # 随机生成n个进程进行运行
    for i in range(process_num):
        # 每个进程均采用最简单的配置，不额外设置需要的资源，特殊资源，特殊事件，这里每个进程的优先级都是随机的
        temp_process = MyProcess(name="p" + str(i), work_time=random.randint(1, 10), priority=random.randint(1, 10),resource=[],event=[],special_resource=[0,{}],thread_flag=0)
        # 不对进程需要的内存页面进行设置
        temp_process.set_page_access_list(page_access_list=[],page_number=0)
        processes.append(temp_process)
    os = MyOS(processes=processes, process_scheduling_algorithm=1, available=[0,0,0],buffer_size=5,memory_size=100,memory_number=10)
    # 另开一个线程来运行os
    os_thread = threading.Thread(target=os.run)
    os_thread.start()
    while True:
        command = Command()
        command.print_process_queue(os)
        print()
        time.sleep(2)

# 基于时间片轮转法的进程互斥测试
def auto_process_mutual_exclusion_test(time_slice: int):
    p0 = MyProcess(name="p0", work_time=4, priority=1, resource={
        0: [0, 0, 0]
    }, event=[2], special_resource=[1, {}],thread_flag=0)
    p1 = MyProcess(name="p1", work_time=4, priority=1, resource={
        0: [0, 0, 0]
    }, event=[1], special_resource=[1, {}],thread_flag=0)
    p2 = MyProcess(name="p2", work_time=4, priority=1, resource={
        0: [0, 0, 0]
    }, event=[1], special_resource=[1, {}],thread_flag=0)
    p3 = MyProcess(name="p3", work_time=4, priority=1, resource={
        0: [0, 0, 0]
    }, event=[2], special_resource=[1, {}],thread_flag=0)
    p4 = MyProcess(name="p4", work_time=4, priority=1, resource={
        0: [0, 0, 0]
    }, event=[2], special_resource=[1, {}],thread_flag=0)
    p0.set_page_access_list(page_access_list=[],page_number=0)
    p1.set_page_access_list(page_access_list=[],page_number=0)
    p2.set_page_access_list(page_access_list=[],page_number=0)
    p3.set_page_access_list(page_access_list=[],page_number=0)
    p4.set_page_access_list(page_access_list=[],page_number=0)
    processes = [p0, p1, p2, p3, p4]
    os = MyOS(processes=processes, process_scheduling_algorithm=0, available=[0, 0, 0], buffer_size=5,memory_size=100,memory_number=10,
              time_slice=time_slice)
    # 另开一个线程来运行os
    os_thread = threading.Thread(target=os.run)
    os_thread.start()
    while True:
        command = Command()
        command.print_process_queue(os)
        print()
        command.print_buffer(os)
        print()
        time.sleep(2)


# 基于时间片轮转法的进程同步测试
def auto_process_synchronization_test(time_slice: int):
    p0 = MyProcess(name="p0", work_time=10, priority=1, resource={
        0: [0, 0, 0]
    }, event=[3], special_resource=[0, {3: "p1"}],thread_flag=0)
    p1 = MyProcess(name="p1", work_time=10, priority=1, resource={
        0: [0, 0, 0]
    }, event=[3], special_resource=[0, {}],thread_flag=0)
    p0.set_page_access_list(page_access_list=[], page_number=0)
    p1.set_page_access_list(page_access_list=[], page_number=0)
    processes = [p0, p1]
    os = MyOS(processes=processes, process_scheduling_algorithm=0, available=[0, 0, 0], buffer_size=5,memory_size=100,memory_number=10,
              time_slice=time_slice)
    # 另开一个线程来运行os
    os_thread = threading.Thread(target=os.run)
    os_thread.start()
    while True:
        command = Command()
        command.print_process_queue(os)
        print()
        time.sleep(2)


# 基于时间片轮转法的进程通信测试
def auto_process_communicate_test(time_slice: int):
    p0 = MyProcess(name="p0", work_time=10, priority=1, resource={
        0: [0, 0, 0]
    }, event=[4], special_resource=[0, {}],thread_flag=0)
    p1 = MyProcess(name="p1", work_time=10, priority=1, resource={
        0: [0, 0, 0]
    }, event=[4], special_resource=[0, {}],thread_flag=0)
    p0.set_message([
        [1, p1, "nice to meet you"],
        [9, p1, "see you to tomorrow"]
    ])
    p1.set_message([
        [1, p0, "nice to meet you too"],
        [9, p0, "see you to tomorrow too"]
    ])
    p0.set_page_access_list(page_access_list=[], page_number=0)
    p1.set_page_access_list(page_access_list=[], page_number=0)
    processes = [p0, p1]
    os = MyOS(processes=processes, process_scheduling_algorithm=0, available=[0, 0, 0], buffer_size=5,memory_size=100,memory_number=10,
              time_slice=time_slice)
    # 另开一个线程来运行os
    os_thread = threading.Thread(target=os.run)
    os_thread.start()
    while True:
        command = Command()
        command.print_process_queue(os)
        print()
        command.print_cpu_log(os)
        print()
        command.print_process_receive_message(os)
        print()
        time.sleep(3)


# 基于时间片轮转法进程调度的死锁处理测试
def auto_deadlock_handling_test(time_slice: int):
    p0 = MyProcess(name="p0", work_time=10, priority=1, resource={
        0: [0, 1, 0],
        3: [7, 4, 3]
    }, event=0, special_resource=[0, {}],thread_flag=0)
    p1 = MyProcess(name="p1", work_time=10, priority=1, resource={
        0: [2, 0, 0],
        3: [1, 2, 2]
    }, event=0, special_resource=[0, {}],thread_flag=0)
    p2 = MyProcess(name="p2", work_time=10, priority=1, resource={
        0: [3, 0, 2],
        3: [6, 0, 0]
    }, event=0, special_resource=[0, {}],thread_flag=0)
    p3 = MyProcess(name="p3", work_time=10, priority=1, resource={
        0: [2, 1, 1],
        3: [0, 1, 1]
    }, event=0, special_resource=[0, {}],thread_flag=0)
    p4 = MyProcess(name="p4", work_time=10, priority=1, resource={
        0: [0, 0, 2],
        3: [4, 3, 1]
    }, event=0, special_resource=[0, {}],thread_flag=0)
    p0.set_page_access_list(page_access_list=[], page_number=0)
    p1.set_page_access_list(page_access_list=[], page_number=0)
    p2.set_page_access_list(page_access_list=[], page_number=0)
    p3.set_page_access_list(page_access_list=[], page_number=0)
    p4.set_page_access_list(page_access_list=[], page_number=0)
    processes = [p0, p1, p2, p3, p4]
    os = MyOS(processes=processes, process_scheduling_algorithm=0, available=[10, 5, 7],buffer_size=5,memory_size=100,memory_number=10, time_slice=time_slice)
    # 另开一个线程来运行os
    os_thread = threading.Thread(target=os.run)
    os_thread.start()
    while True:
        command = Command()
        command.print_process_queue(os)
        print()
        command.print_resource_allocation_log(os)
        time.sleep(2)


# 基于时间片轮转法的内存分配和回收测试
def auto_memory_allocation_and_recycling_test(time_slice: int):
    p0 = MyProcess(name="p0", work_time=10, priority=1, resource={
        0: [0, 0, 0]
    }, event=[], special_resource=[0, {}], thread_flag=0)
    p1 = MyProcess(name="p1", work_time=10, priority=1, resource={
        0: [0, 0, 0]
    }, event=[], special_resource=[0, {}], thread_flag=0)
    p2 = MyProcess(name="p2", work_time=10, priority=1, resource={
        0: [0, 0, 0]
    }, event=[], special_resource=[0, {}], thread_flag=0)
    p3 = MyProcess(name="p3", work_time=10, priority=1, resource={
        0: [0, 0, 0]
    }, event=[], special_resource=[0, {}], thread_flag=0)
    p4 = MyProcess(name="p4", work_time=10, priority=1, resource={
        0: [0, 0, 0]
    }, event=[], special_resource=[0, {}], thread_flag=0)
    p0.set_page_access_list(page_access_list=[], page_number=0)
    p1.set_page_access_list(page_access_list=[], page_number=0)
    p2.set_page_access_list(page_access_list=[], page_number=0)
    p3.set_page_access_list(page_access_list=[], page_number=0)
    p4.set_page_access_list(page_access_list=[], page_number=0)
    processes = [p0, p1, p2, p3, p4]
    os = MyOS(processes=processes, process_scheduling_algorithm=0, available=[0, 0, 0], buffer_size=5, memory_size=100,
              memory_number=10,
              time_slice=time_slice)
    # 另开一个线程来运行os
    os_thread = threading.Thread(target=os.run)
    os_thread.start()
    while True:
        command = Command()
        command.print_process_queue(os)
        print()
        command.print_memory_use(os)
        print()
        time.sleep(2)

# 基于时间片轮转法的内存换入换出测试
def auto_memory_swapping_in_and_out_test(time_slice: int):
    p0 = MyProcess(name="p0", work_time=10, priority=1, resource={
        0: [0, 0, 0]
    }, event=[], special_resource=[0, {}], thread_flag=0)
    p0.set_page_access_list(page_access_list=[
        [0, [0, 1, 2, 3, 4, 5]],
        [3, [6, 7, 8, 9, 10]],
        [4, [11]],
        [5, [12]],
        [6, [13, 14]]
    ], page_number=15)
    processes = [p0]
    os = MyOS(processes=processes, process_scheduling_algorithm=0, available=[0, 0, 0], buffer_size=5, memory_size=100,
              memory_number=10,
              time_slice=time_slice)
    # 另开一个线程来运行os
    os_thread = threading.Thread(target=os.run)
    os_thread.start()
    while True:
        command = Command()
        command.print_page_table(os)
        print()
        command.print_page_access_log(os)
        print()
        time.sleep(2)

# 基于时间片轮转法的外存访问测试
def auto_external_memory_access(time_slice: int):
    p0 = MyProcess(name="p0", work_time=10, priority=1, resource={
        0: [0, 0, 0]
    }, event=[5], special_resource=[0, {}], thread_flag=0)
    p1 = MyProcess(name="p1", work_time=10, priority=1, resource={
        0: [0, 0, 0]
    }, event=[5], special_resource=[0, {}], thread_flag=0)
    p0.set_file_access([
        [1, "./test.txt", "w", "nice to meet you"],
        [9, "./test.txt", "r"]
    ])
    p1.set_file_access([
        [2, "./test.txt", "r"],
        [5, "./test.txt", "w", "see you to tomorrow"]
    ])
    p0.set_page_access_list(page_access_list=[], page_number=0)
    p1.set_page_access_list(page_access_list=[], page_number=0)
    processes = [p0, p1]
    os = MyOS(processes=processes, process_scheduling_algorithm=0, available=[0, 0, 0], buffer_size=5, memory_size=100, memory_number=10,
              time_slice=time_slice)
    # 另开一个线程来运行os
    os_thread = threading.Thread(target=os.run)
    os_thread.start()
    while True:
        command = Command()
        command.print_process_queue(os)
        print()
        command.print_cpu_log(os)
        print()
        command.print_process_read_file_content(os)
        print()
        time.sleep(3)

# 基于时间片轮转法的线程测试
def auto_thread_test(time_slice: int):
    p0 = MyProcess(name="p0", work_time=20, priority=1, resource={}, event=6, special_resource=[0, {}], thread_flag=0)
    processes = [p0]
    p0.set_thread_create_table([
        [0, "p0-t1", 12],
        [5, "p0-t2", 5]
    ])
    p0.set_page_access_list(page_access_list=[], page_number=0)
    os = MyOS(processes=processes, process_scheduling_algorithm=0, available=[0, 0, 0], buffer_size=5,memory_size=100, memory_number=10,
              time_slice=time_slice)
    os_thread = threading.Thread(target=os.run)
    os_thread.start()
    while True:
        command = Command()
        command.print_process_queue(os)
        print()
        time.sleep(2)


# 基于时间片轮转法的进程挂起和唤醒测试
def suspend_and_activation_test(time_slice: int):
    p0 = MyProcess(name="p0", work_time=10, priority=1, resource={
        0: [0, 0, 0]
    }, event=[3], special_resource=[0, {3: "p1"}], thread_flag=0)
    p1 = MyProcess(name="p1", work_time=10, priority=1, resource={
        0: [0, 0, 0]
    }, event=[3], special_resource=[0, {}], thread_flag=0)
    p0.set_page_access_list(page_access_list=[], page_number=0)
    p1.set_page_access_list(page_access_list=[], page_number=0)
    processes = [p0, p1]
    os = MyOS(processes=processes, process_scheduling_algorithm=0, available=[0, 0, 0], buffer_size=5, memory_size=100,
              memory_number=10,
              time_slice=time_slice)
    # 另开一个线程来运行os
    os_thread = threading.Thread(target=os.run)
    os_thread.start()
    while True:
        command = Command()
        if os.os_time == 4:
            command.suspend(os,"p0")
        elif os.os_time == 15:
            command.activation(os,"p0")
        command.print_process_queue(os)
        print()
        time.sleep(1)

def auto_comprehensive_test(time_slice: int):
    p1 = MyProcess(name="p1", work_time=10, priority=1, resource={
        0: [0, 1, 0],
        3:[7,4,3]
    }, event=[5], special_resource=[0, {}], thread_flag=0)
    p2 = MyProcess(name="p2", work_time=10, priority=1, resource={
        0: [2, 0, 0],
        3:[1,2,2]
    }, event=[5], special_resource=[0, {}], thread_flag=0)
    p1.set_message([
        [1, p2, "nice to meet you"],
        [4, p2, "see you to tomorrow"]
    ])
    p2.set_message([
        [2, p1, "nice to meet you too"],
        [5, p1, "see you to tomorrow too"]
    ])
    p1.set_file_access([
        [1, "./test.txt", "w", "nice to meet you"],
        [9, "./test.txt", "r"]
    ])
    p2.set_file_access([
        [2, "./test.txt", "r"],
        [5, "./test.txt", "w", "see you to tomorrow"]
    ])
    p1.set_page_access_list(page_access_list=[

    ], page_number=0)
    p2.set_page_access_list(page_access_list=[

    ], page_number=0)
    processes = [p1,p2]
    os = MyOS(processes=processes, process_scheduling_algorithm=0, available=[5, 5, 5], buffer_size=5, memory_size=100,
              memory_number=10,
              time_slice=time_slice)
    # 另开一个线程来运行os
    os_thread = threading.Thread(target=os.run)
    os_thread.start()
    while True:
        command = Command()
        command.print_process_queue(os)
        print()
        command.print_cpu_log(os)
        print()

        time.sleep(2)

# 时间片轮转法进程调度测试
def time_slice_rotation_test(time_slice: int, process_num: int):
    processes = []
    # 随机生成n个进程进行运行
    for i in range(process_num):
        # 每个进程均采用最简单的配置，不额外设置需要的资源，特殊资源，特殊事件
        temp_process = MyProcess(name="p" + str(i), work_time=random.randint(1, 10), priority=1,resource=[],event=[],special_resource=[0,{}],thread_flag=0)
        # 不对进程需要的内存页面进行设置
        temp_process.set_page_access_list(page_access_list=[],page_number=0)
        processes.append(temp_process)
    os = MyOS(processes=processes, process_scheduling_algorithm=0, available=[0,0,0],buffer_size=5,memory_size=100,memory_number=10,time_slice=time_slice)
    # 另开一个线程来运行os
    os_thread = threading.Thread(target=os.run)
    os_thread.start()
    return os