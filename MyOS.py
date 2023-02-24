# -*- coding: utf-8 -*-
"""
@author yumu
@className myOS
@version 1.0.0
@describe TODO 1 修改测试函数 2 线程和进程的运行关系 3 输出内存使用表
"""

from MyCPU import *
from Resource import *
from MyProcess import *
import queue


class MyOS:
    # 就绪队列
    process_queue = queue.PriorityQueue()
    # 创建态队列
    create_process_queue = []
    # 终止态队列
    terminated_process_queue = []
    # 挂起队列
    suspend_process_queue = []
    # 阻塞态队列
    block_process_queue = []
    # 资源池
    resource_pool = []
    # 系统时间
    os_time = 0
    # cpu
    cpu = MyCPU()
    # 进程调度算法
    # 0对应时间片轮转法
    # 1对应非抢占式静态优先级调度
    process_scheduling_algorithm = None
    # 时间片大小
    time_slice = 2
    # 装各个队列信息的列表
    print_process_queue = []
    # 状态列表
    process_state_table = ["创建态", "就绪态", "运行态", "阻塞态", "终止态"]
    # 资源分配类
    resource_allocation = Resource_allocation()
    # 缓冲区
    buffer = []
    # 缓冲区大小
    buffer_size = None
    # 互斥信号量
    mutex = 1
    # 进程表
    process_table = []
    # 内存大小
    memory_size = None
    # 内存分块数量
    memory_number = None
    # 用户内存起点
    memory_user_start = 20
    # 内存使用表
    memory_use_table = []
    # 页面访问记录
    page_access_log = []

    def __init__(self, processes, process_scheduling_algorithm, available, buffer_size, memory_size, memory_number,
                 time_slice=2):
        self.process_scheduling_algorithm = process_scheduling_algorithm
        self.time_slice = time_slice
        self.resource_allocation.available = available
        self.buffer_size = buffer_size
        self.process_table = processes
        self.memory_size = memory_size
        self.memory_number = memory_number
        for process in processes:
            self.resource_allocation.resource_allocation_table.update({
                process.PCB['name']: process
            })
            self.create_process_queue.append(process)
        self.create_memory_use_table()

    # 页表请求机制，用于调入页面或者置换页面
    def page_table_request_mechanism(self, page_access_list):
        # 将要请求的页表一个个取出来
        for page in page_access_list[1]:
            # 如果当前要请求的页面不在内存中
            if self.cpu.process_in_cpu.page_table[page][1] == 0:
                # 如果内存未满
                if self.cpu.process_in_cpu.page_in_memory_number < self.memory_size / self.memory_number:
                    # 查找空内存地址
                    address = None
                    for index in self.cpu.process_in_cpu.memory_use_in_process:
                        if self.cpu.process_in_cpu.memory_use_in_process[index] == 0:
                            address = index
                            break
                    # 给页面分配内存地址
                    self.cpu.process_in_cpu.page_table[page][0] = address
                    # 将页面调入内存
                    self.cpu.process_in_cpu.page_table[page][1] = 1
                    # 将内存中的页数加一
                    self.cpu.process_in_cpu.page_in_memory_number += 1
                    # 将其访问字段加一
                    self.cpu.process_in_cpu.page_table[page][2] += 1
                    # 把调入的页面记录到栈
                    self.cpu.process_in_cpu.page_stack.append(page)
                    self.page_access_log.append(
                        str(self.os_time) + "时刻" + " 进程" + self.cpu.process_in_cpu.PCB['name'] + "调入页面" + str(page))
                else:
                    first_in_page_index = self.cpu.process_in_cpu.page_stack[0]
                    del self.cpu.process_in_cpu.page_stack[0]
                    self.cpu.process_in_cpu.page_stack.append(page)
                    # 将要换出的页面的状态位置为0
                    self.cpu.process_in_cpu.page_table[first_in_page_index][1] = 0
                    # 将要换出的页面的使用次数置为0
                    self.cpu.process_in_cpu.page_table[first_in_page_index][2] = 0
                    # 调入的页面使用调出的页面的内存地址
                    self.cpu.process_in_cpu.page_table[page][0] = self.cpu.process_in_cpu.page_table[first_in_page_index][0]
                    self.cpu.process_in_cpu.page_table[first_in_page_index][0] = None
                    # 将请求的页面调入内存
                    self.cpu.process_in_cpu.page_table[page][1] = 1
                    # 将其访问字段加一
                    self.cpu.process_in_cpu.page_table[page][2] += 1
                    self.page_access_log.append(
                        str(self.os_time) + "时刻" + " 进程" + self.cpu.process_in_cpu.PCB['name'] + "换出页面" + str(
                            first_in_page_index) + "换入页面" + str(page))
            # 如果当前请求的页面在内存中,则直接将其访问字段加一,不需要调入页面
            elif self.cpu.process_in_cpu.page_table[page][1] == 1:
                self.cpu.process_in_cpu.page_table[page][2] += 1

    def create_memory_use_table(self):
        for i in range(self.memory_number + 1):
            self.memory_use_table.append([i + 1, self.memory_size / self.memory_number,
                                          self.memory_user_start + i * (self.memory_size / self.memory_number), 0,
                                          None])

    def message_passing(self, process: MyProcess, message):
        process.message_receive.append(message)

    def external_memory_access(self, file_access):
        if file_access[2] == "r":
            with open(file_access[1], "r") as f:
                for i in f:
                    i.strip()
                    self.cpu.process_in_cpu.file_read.append(i)
            self.cpu.cpu_log.append(
                str(self.os_time) + "时刻" + self.cpu.process_in_cpu.PCB['name'] + "读取文件" + file_access[1])
        elif file_access[2] == "w":
            with open(file_access[1], "w") as f:
                f.write(file_access[3])
            self.cpu.cpu_log.append(
                str(self.os_time) + "时刻" + self.cpu.process_in_cpu.PCB['name'] + "向文件" + file_access[1] + "中写入内容" +
                file_access[3])

    def security_algorithm(self, copy_dict, available) -> bool:
        self.resource_allocation.safety_sequence.clear()
        flag = 1
        # 获取资源分配表长度
        process_length = len(copy_dict)
        while len(copy_dict) != 0:
            for process_name in copy_dict:
                for i in range(len(copy_dict[process_name].still_need)):
                    if copy_dict[process_name].still_need[i] > available[i]:
                        flag = 0
                        break
                if flag == 0:
                    flag = 1
                    continue
                available = available
                for i in range(len(copy_dict[process_name].allocation)):
                    available[i] += copy_dict[process_name].allocation[i]
                self.resource_allocation.safety_sequence.append(process_name)
                del copy_dict[process_name]
                break
        if len(self.resource_allocation.safety_sequence) == process_length:
            self.resource_allocation.resource_allocation_log.append(
                "存在安全序列" + str(self.resource_allocation.safety_sequence) + "可以分配")
            return True
        else:
            self.resource_allocation.resource_allocation_log.append("不存在安全序列,不能分配")
            return False

    def banker_algorithm(self, process: MyProcess, request: list) -> bool:
        self.resource_allocation.resource_allocation_log.append(
            str(self.os_time) + "时刻" + process.PCB['name'] + "请求资源" + str(request))
        # 第一步
        for i in range(len(request)):
            if request[i] > process.still_need[i]:
                self.resource_allocation.resource_allocation_log.append(process.PCB['name'] + "请求的资源数大于最多还需要的资源数，出错")
                return False

        # 第二步
        for i in range(len(request)):
            if request[i] > self.resource_allocation.available[i]:
                self.resource_allocation.resource_allocation_log.append("系统尚无足够资源" + process.PCB['name'] + "必须等待")
                return False
        # 第三步，修改相应的数据，为执行安全性算法做准备
        for i in range(len(request)):
            process.allocation[i] += request[i]
            process.still_need[i] -= request[i]
            self.resource_allocation.available[i] -= request[i]

        copy_dict = copy.deepcopy(self.resource_allocation.resource_allocation_table)
        copy_dict[process.PCB['name']] = process
        security_algorithm_result = self.security_algorithm(copy_dict, self.resource_allocation.available)
        if security_algorithm_result:
            return True
        else:
            # 还原数据
            for i in range(len(request)):
                process.allocation[i] -= request[i]
                process.still_need[i] += request[i]
                self.resource_allocation.available[i] += request[i]
            return False

    def return_resource(self, process: MyProcess):
        for i in range(len(process.allocation)):
            self.resource_allocation.available[i] += process.allocation[i]

    def check_special_resource(self, process: MyProcess, time_slice: int):
        flag = True
        resource_needed = []
        if process.special_resource[0] == 1:
            if process.use_buffer == 1:
                flag = True
            elif (1 in process.event and len(self.buffer) < self.buffer_size and self.mutex == 1) or (
                    2 in process.event and len(self.buffer) > 0 and self.mutex == 1):
                flag = True
                resource_needed.append(0)
            else:
                flag = False
        process_time = process.PCB['total_work_time'] - process.PCB['work_time']
        for i in range(time_slice):
            process_time += i
            if process_time in process.special_resource[1]:
                if len(self.terminated_process_queue) == 0:
                    flag = False
                for terminated_process in self.terminated_process_queue:
                    if terminated_process.PCB['name'] == process.special_resource[1][process_time]:
                        flag = True
                        resource_needed.append(1)
                    else:
                        flag = False
        return flag, resource_needed

    def check_simple_resource(self, process: MyProcess, flag, time_slice: int = None):
        '''
        :param process: 需要进行一般资源检查的进程
        :param flag: 用于标识是时间片轮转法还是静态优先级调度 1 时间片轮转法 2 静态优先级调度
        :return:
        '''
        if flag == 1:
            check_result = True
            create_process_time = process.PCB['total_work_time'] - process.PCB['work_time']
            for i in range(time_slice):
                create_process_time += i
                if create_process_time in process.PCB['resource']:
                    if self.banker_algorithm(process, process.PCB['resource'][create_process_time]):
                        check_result = True
                    else:
                        check_result = False
                else:
                    check_result = True
            return check_result
        # 如果是静态优先级调度的话就需要同时检查该进程需要的全部资源是否能一次性分配
        elif flag==2:
            return self.banker_algorithm(process, process.max_need)

    def memory_allocation(self, process: MyProcess):
        # 遍历内存使用表
        for index in range(len(self.memory_use_table)):
            # 如果有空闲内存分区
            if self.memory_use_table[index][3] == 0:
                # 将该内存分区分配给该进程
                self.memory_use_table[index][3] = 1
                # 记录内存分配信息
                self.memory_use_table[index][4] = process
                # 在进程中记录分配得到的内存编号
                process.memory_number = index + 1
                # 准备初始化页表
                page_table = []
                # 初始化进程内部内存使用表
                memory_use_in_process = {}
                for i in range(int(self.memory_size / self.memory_number)):
                    memory_use_in_process.update({self.memory_use_table[index][2] + i: 0})
                # 遍历进程需要的页面
                for i in range(process.page_number):
                    # 如果内存装的下，直接调入内存
                    if i < self.memory_number:
                        page_table.append([self.memory_use_table[index][2] + i, 1, 0, 0, "x"])
                        # 把该内存标记为已经使用
                        memory_use_in_process[self.memory_use_table[index][2] + i] = 1
                        # 在内存中的页面数加一
                        process.page_in_memory_number += 1
                        # 向页面栈加入记录
                        process.page_stack.append(i)
                    # 如果装不下则放在外存
                    else:
                        page_table.append([None, 0, 0, 0, "x"])
                # 更新页表
                process.set_page_table(page_table)
                process.memory_use_in_process = memory_use_in_process
                return True
        return False

    def check_resource(self, process, queue_flag):
        '''
        :param process: 要进行资源检查的进程
        :param queue_flag:
        1 时间片轮转法情况下的创建态进程的资源检查
        2 时间片轮转法情况下的阻塞态进程的资源检查
        3 时间片轮转法运行中进程资源检查
        4 静态优先级调度情况下的资源检查
        :return:
        '''
        flag, resource_needed = self.check_special_resource(process, time_slice=self.time_slice)
        if queue_flag == 4:
            if flag and self.check_simple_resource(process=process, flag=2):
                if self.memory_allocation(process):
                    if 0 in resource_needed:
                        process.use_buffer = 1
                        self.mutex -= 1
                    process.PCB['state'] = 1
                    self.process_queue.put(process)
                    descending_list = []
                    while not self.process_queue.empty():
                        descending_list.append(self.process_queue.get())
                    for i in range(len(descending_list)-1):
                        for j in range(len(descending_list)-1-i):
                            if descending_list[i].priority > descending_list[i+1].priority:
                                temp = descending_list[i]
                                descending_list[i] = descending_list[i+1]
                                descending_list[i + 1] = temp
                    for i in descending_list:
                        self.process_queue.put(i)
                    self.create_process_queue.remove(process)
        elif queue_flag == 3:
            # 已经上机运行过的进程不需要再做特殊资源的判断
            if flag and self.check_simple_resource(process=process, flag=1, time_slice=self.time_slice):
                self.cpu.process_in_cpu.PCB['state'] = 1
                self.process_queue.put(self.cpu.process_in_cpu)
                self.cpu.process_in_cpu = None
            else:
                self.cpu.process_in_cpu.PCB['state'] = 3
                self.block_process_queue.append(self.cpu.process_in_cpu)
                self.cpu.process_in_cpu = None
        elif flag and self.check_simple_resource(process=process, flag=1, time_slice=self.time_slice):
            if self.memory_allocation(process):
                if 0 in resource_needed:
                    process.use_buffer = 1
                    self.mutex -= 1
                process.PCB['state'] = 1
                self.process_queue.put(process)
                if queue_flag == 1:
                    self.create_process_queue.remove(process)
                elif queue_flag == 2:
                    self.block_process_queue.remove(process)

    def return_buffer(self):
        # 查看当前进程是否有使用缓冲区
        if self.cpu.process_in_cpu.use_buffer == 1:
            # 标记为未使用缓冲区
            self.cpu.process_in_cpu.use_buffer = 0
            # 信号量加1
            self.mutex += 1
            # 判断进程对应的行为，对缓冲区进行相关操作
            if 1 in self.cpu.process_in_cpu.event:
                self.buffer.append(1)
            elif 2 in self.cpu.process_in_cpu.event:
                self.buffer.remove(len(self.buffer))

    def return_memory(self):
        self.memory_use_table[self.cpu.process_in_cpu.memory_number - 1][3] = 0
        self.memory_use_table[self.cpu.process_in_cpu.memory_number - 1][4] = None

    def check_process_to_queue(self, operating_mode):
        '''
        :param operating_mode: 指定cpu运行模式 1 时间片轮转 2 静态优先级调度
        :return:
        '''
        if operating_mode == 1:
            # 查看创建完成的进程是否有可以进入就绪队列的
            for create_process in self.create_process_queue:
                self.check_resource(create_process, 1)
            # 查看阻塞队列中的进程是否有可以进入就绪队列的
            for block_process in self.block_process_queue:
                self.check_resource(block_process, 2)
        elif operating_mode == 2:
            # 查看创建完成的进程是否有可以进入就绪队列的
            # copy_dict = copy.deepcopy(self.create_process_queue)
            for create_process in self.create_process_queue:
                self.check_resource(create_process, 4)

    def update_queue_info(self):
        # 更新当前进程队列状态
        print_process_queue_dict = []
        if len(self.create_process_queue) == 0:
            print_process_queue_dict.append("创建态进程队列为空")
        else:
            print_process_queue_dict.append("创建态进程队列如下")
            for process in self.create_process_queue:
                if process.thread_flag == 0:
                    print_process_queue_dict.append(
                        "进程" + process.PCB['name'] + " 需要使用处理机的时间为:" + str(process.PCB['work_time']) + "优先级为:" + str(
                            process.PCB['priority']) + "处于的状态是:" + self.process_state_table[process.PCB['state']])
                elif process.thread_flag == 1:
                    print_process_queue_dict.append(
                        "线程" + process.PCB['name'] + "属于进程" + process.main_process.PCB['name'] + " 需要使用处理机的时间为:" + str(
                            process.PCB['work_time']) + "优先级为:" + str(
                            process.PCB['priority']) + "处于的状态是:" + self.process_state_table[process.PCB['state']])
        if len(self.process_queue.queue) == 0:
            print_process_queue_dict.append("就绪进程队列为空")
        else:
            print_process_queue_dict.append("就绪进程队列如下")
            for process in self.process_queue.queue:
                if process.thread_flag == 0:
                    print_process_queue_dict.append(
                        "进程" + process.PCB['name'] + " 需要使用处理机的时间为:" + str(process.PCB['work_time']) + "优先级为:" + str(
                            process.PCB['priority']) + "处于的状态是:" + self.process_state_table[process.PCB['state']])
                elif process.thread_flag == 1:
                    print_process_queue_dict.append(
                        "线程" + process.PCB['name'] + "属于进程" + process.main_process.PCB['name'] + " 需要使用处理机的时间为:" + str(
                            process.PCB['work_time']) + "优先级为:" + str(
                            process.PCB['priority']) + "处于的状态是:" + self.process_state_table[process.PCB['state']])
        if len(self.block_process_queue) == 0:
            print_process_queue_dict.append("阻塞态进程队列为空")
        else:
            print_process_queue_dict.append("阻塞态进程队列如下")
            for process in self.block_process_queue:
                if process.thread_flag == 0:
                    print_process_queue_dict.append(
                        "进程" + process.PCB['name'] + " 需要使用处理机的时间为:" + str(process.PCB['work_time']) + "优先级为:" + str(
                            process.PCB['priority']) + "处于的状态是:" + self.process_state_table[process.PCB['state']])
                elif process.thread_flag == 1:
                    print_process_queue_dict.append(
                        "线程" + process.PCB['name'] + "属于进程" + process.main_process.PCB['name'] + " 需要使用处理机的时间为:" + str(
                            process.PCB['work_time']) + "优先级为:" + str(
                            process.PCB['priority']) + "处于的状态是:" + self.process_state_table[process.PCB['state']])
        if len(self.terminated_process_queue) == 0:
            print_process_queue_dict.append("终止态进程队列为空")
        else:
            print_process_queue_dict.append("终止态进程队列如下")
            for process in self.terminated_process_queue:
                if process.thread_flag == 0:
                    print_process_queue_dict.append(
                        "进程" + process.PCB['name'] + " 需要使用处理机的时间为:" + str(process.PCB['work_time']) + "优先级为:" + str(
                            process.PCB['priority']) + "处于的状态是:" + self.process_state_table[process.PCB['state']])
                elif process.thread_flag == 1:
                    print_process_queue_dict.append(
                        "线程" + process.PCB['name'] + "属于进程" + process.main_process.PCB['name'] + " 需要使用处理机的时间为:" + str(
                            process.PCB['work_time']) + "优先级为:" + str(
                            process.PCB['priority']) + "处于的状态是:" + self.process_state_table[process.PCB['state']])
        if self.cpu.process_in_cpu == None:
            print_process_queue_dict.append("现在无正在上机的进程")
        else:
            if self.cpu.process_in_cpu.thread_flag == 1:
                print_process_queue_dict.append("现在正在上机的线程为" + self.cpu.process_in_cpu.PCB['name'] + "属于进程" +
                                                self.cpu.process_in_cpu.main_process.PCB['name'])
            elif self.cpu.process_in_cpu.use_buffer == 1:
                print_process_queue_dict.append("现在正在上机的进程为" + self.cpu.process_in_cpu.PCB['name'] + "该进程正在使用缓冲区")
            else:
                print_process_queue_dict.append("现在正在上机的进程为" + self.cpu.process_in_cpu.PCB['name'])
        if len(self.suspend_process_queue) == 0:
            print_process_queue_dict.append("挂起进程队列为空")
        else:
            print_process_queue_dict.append("挂起进程队列如下")
            state = None
            for process in self.suspend_process_queue:
                if self.process_state_table[process.PCB['state']] == 1:
                    state = "静止就绪"
                elif self.process_state_table[process.PCB['state']] == 3:
                    state = "静止阻塞"
                print_process_queue_dict.append(
                    "进程" + process.PCB['name'] + " 需要使用处理机的时间为:" + str(process.PCB['work_time']) + "优先级为:" + str(
                        process.PCB['priority']) + "处于的状态是:" + state)
        self.print_process_queue = print_process_queue_dict

    def os_run_with_time_slice(self):
        # 时间片用完退出处理机的情况
        if self.cpu.time_slice_used == self.cpu.time_slice:
            self.cpu.time_slice_used = 0
            self.os_time -= 1
            # 判断当前上机进程是否执行完毕，若没有完成，还需再次入队
            if self.cpu.process_in_cpu.PCB['work_time'] > 0:
                self.check_resource(process=self.cpu.process_in_cpu, queue_flag=3)
            else:
                self.return_buffer()
                self.return_memory()
                self.cpu.process_in_cpu.PCB['state'] = 4
                self.terminated_process_queue.append(self.cpu.process_in_cpu)
                self.return_resource(self.cpu.process_in_cpu)
                self.cpu.process_in_cpu = None

        # 时间片未用完退出处理机的情况
        else:
            if self.cpu.process_in_cpu != None:
                self.return_buffer()
                self.return_memory()
                self.cpu.process_in_cpu.PCB['state'] = 4
                self.terminated_process_queue.append(self.cpu.process_in_cpu)
                self.return_resource(self.cpu.process_in_cpu)
                self.cpu.process_in_cpu = None
            # 继续取下一个进程上机
            if not self.process_queue.empty():
                process = self.process_queue.get()
                # 上机前要对cpu进行初始化
                self.cpu.flag = 0
                process.PCB['state'] = 2
                self.cpu.process_in_cpu = process
                self.cpu.os_time = self.os_time
                self.cpu.time_slice = self.time_slice
                self.os_time = self.cpu.run_with_time_slice(self)

    def os_run_with_static_priority(self):
        if self.cpu.process_in_cpu != None:
            self.return_buffer()
            self.return_memory()
            self.cpu.process_in_cpu.PCB['state'] = 4
            self.terminated_process_queue.append(self.cpu.process_in_cpu)
            self.return_resource(self.cpu.process_in_cpu)
            self.cpu.process_in_cpu = None
        if not self.process_queue.empty():
            process = self.process_queue.get()
            # 上机前要对cpu进行初始化
            self.cpu.flag = 0
            process.PCB['state'] = 2
            self.cpu.process_in_cpu = process
            self.cpu.os_time = self.os_time
            self.cpu.time_slice = self.time_slice
            self.os_time = self.cpu.run_with_static_priority(self)

    def run(self):
        while True:
            # 根据进程调度方式来执行对应代码
            if self.process_scheduling_algorithm == 0:
                # operating_mode = 1指定为时间片轮转法
                self.check_process_to_queue(operating_mode=1)
                self.update_queue_info()
                self.os_run_with_time_slice()
            elif self.process_scheduling_algorithm == 1:
                # operating_mode = 2指定为静态优先级调度
                self.check_process_to_queue(operating_mode=2)
                self.update_queue_info()
                self.os_run_with_static_priority()
            self.os_time += 1
            time.sleep(1)
