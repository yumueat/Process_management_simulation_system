# -*- coding: utf-8 -*-
"""
@author yumu
@className myOS
@version 1.0.0
@describe TODO
"""

from MyCPU import *
from Resource import *
from MyProcess import *
import queue
class MyOS:
    process_queue = queue.PriorityQueue()
    create_process_queue = []
    terminated_process_queue = []
    block_process_queue = []
    resource_pool = []
    os_time = 0
    cpu = MyCPU()
    # 进程调度算法
    # 0对应时间片轮转法
    # 1对应非抢占式静态优先级调度
    process_scheduling_algorithm = None
    time_slice = 2
    print_process_queue = []
    process_state_table = ["创建态","就绪态","运行态","阻塞态","终止态"]
    resource_allocation = Resource_allocation()
    buffer = []
    buffer_size = None
    mutex = 1
    def __init__(self,processes,process_scheduling_algorithm,available,buffer_size,time_slice =2):
        self.process_scheduling_algorithm = process_scheduling_algorithm
        self.time_slice = time_slice
        self.resource_allocation.available = available
        self.buffer_size = buffer_size
        for process in processes:
            self.resource_allocation.resource_allocation_table.update({
                process.PCB['name']:process
            })
            self.create_process_queue.append(process)
    def security_algorithm(self,copy_dict,available) ->bool:
        self.resource_allocation.safety_sequence.clear()
        flag = 1
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
            self.resource_allocation.resource_allocation_log.append("存在安全序列"+str(self.resource_allocation.safety_sequence) + "可以分配")
            return True
        else:
            self.resource_allocation.resource_allocation_log.append("不存在安全序列,不能分配")
            return False

    def banker_algorithm(self,process:MyProcess,request:list)->bool:
        self.resource_allocation.resource_allocation_log.append(
            str(self.os_time) + "时刻" + process.PCB['name'] + "请求资源" + str(request))
        # 第一步
        for i in range(len(request)):
            if request[i] > process.still_need[i]:
                self.resource_allocation.resource_allocation_log.append( process.PCB['name'] + "请求的资源数大于最多还需要的资源数，出错")
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

        copy_dict =  self.resource_allocation.resource_allocation_table
        copy_dict[process.PCB['name']] = process
        security_algorithm_result =  self.security_algorithm(copy_dict, self.resource_allocation.available)
        if security_algorithm_result:
            return True
        else:
            # 还原数据
            for i in range(len(request)):
                process.allocation[i] -= request[i]
                process.still_need[i] += request[i]
                self.resource_allocation.available[i] += request[i]
            return False

    def return_resource(self,process:MyProcess):
        for i in range(len(process.allocation)):
            self.resource_allocation.available[i] += process.allocation[i]

    def check_special_resource(self,process:MyProcess):
        flag = False
        resource_needed = []
        if process.special_resource[0] == 1:
            if (process.event == 1 and len(self.buffer) < self.buffer_size and self.mutex == 1) or (process.event == 2 and len(self.buffer) > 0 and self.mutex ==1):
                flag =True
                resource_needed.append(0)
        process_time = process.PCB['total_work_time'] - process.PCB['work_time']
        if process_time in process.special_resource[1]:
            for terminated_process in self.terminated_process_queue:
                if terminated_process.PCB['name'] == process.special_resource[1][process_time]:
                    flag = True
                    resource_needed.append(1)
                else:
                    flag = False
        return flag,resource_needed

    def check_simple_resource(self,process:MyProcess):
        create_process_time = process.PCB['total_work_time'] - process.PCB['work_time']
        if create_process_time in process.PCB['resource']:
            if self.banker_algorithm(process, process.PCB['resource'][create_process_time]):
                return True
            else:
                return False
        else:
            return True

    def check_resource(self,process,queue_flag):
        '''
        :param process: 要进行资源检查的进程
        :param queue_flag:
        1 创建态进程的资源检查
        2 阻塞态进程的资源检查
        3 时间片轮转法运行中进程资源检查
        :return:
        '''
        flag,resource_needed = self.check_special_resource(process)
        if queue_flag == 3:
            # 已经上机运行过的进程不需要再做特殊资源的判断
            if self.check_simple_resource(process):
                self.cpu.process_in_cpu.PCB['state'] = 1
                self.process_queue.put(self.cpu.process_in_cpu)
                self.cpu.process_in_cpu = None
            else:
                self.cpu.process_in_cpu.PCB['state'] = 3
                self.block_process_queue.append(self.cpu.process_in_cpu)
                self.cpu.process_in_cpu = None
        elif flag and self.check_simple_resource(process):
            if 0 in resource_needed:
                process.use_buffer = 1
                self.mutex -= 1
            process.PCB['state'] = 1
            self.process_queue.put(process)
            if queue_flag == 1:
                self.create_process_queue.remove(process)
            elif queue_flag ==2 :
                self.create_process_queue.remove(process)

    def return_buffer(self):
        # 查看当前进程是否有使用缓冲区
        if self.cpu.process_in_cpu.use_buffer == 1:
            # 标记为未使用缓冲区
            self.cpu.process_in_cpu.use_buffer = 0
            # 信号量加1
            self.mutex += 1
            # 判断进程对应的行为，对缓冲区进行相关操作
            if self.cpu.process_in_cpu.event == 1:
                self.buffer.append(1)
            elif self.cpu.process_in_cpu.event == 2:
                self.buffer.remove(len(self.buffer))

    def check_process_to_queue(self,operating_mode):
        '''
        :param operating_mode: 指定cpu运行模式 1 时间片轮转 2 静态优先级调度
        :return:
        '''
        # 查看创建完成的进程是否有可以进入就绪队列的
        for create_process in self.create_process_queue:
            # 查看是否需要使用缓冲区
            self.check_resource(create_process,1)
            # if create_process.special_resource[0] == 1:
            #     # 查看缓冲区是否空闲且是否为空/满
            #     if (create_process.event == 1 and len(self.buffer) < self.buffer_size and self.mutex == 1) or (create_process.event == 2 and len(self.buffer) > 0 and self.mutex ==1):
            #         # 如果缓冲区空闲且其他需要的资源可以分配，则进入就绪队列
            #         create_process_time = create_process.PCB['total_work_time'] - create_process.PCB['work_time']
            #         if create_process_time in create_process.PCB['resource']:
            #             if self.banker_algorithm(create_process, create_process.PCB['resource'][create_process_time]):
            #                 create_process.use_buffer = 1
            #                 self.mutex -=1
            #                 create_process.PCB['state'] = 1
            #                 self.process_queue.put(create_process)
            #                 self.create_process_queue.remove(create_process)
            #         # 如果缓冲区空闲且没有其他需要的资源，则进入就绪队列
            #         else:
            #             create_process.use_buffer = 1
            #             self.mutex -= 1
            #             create_process.PCB['state'] = 1
            #             self.process_queue.put(create_process)
            #             self.create_process_queue.remove(create_process)
            # else:
            #     # 如果不需要使用缓冲区，就直接看其他需要的资源是否可以分配
            #     create_process_time = create_process.PCB['total_work_time'] - create_process.PCB['work_time']
            #     if create_process_time in create_process.PCB['resource']:
            #         if self.banker_algorithm(create_process, create_process.PCB['resource'][create_process_time]):
            #             create_process.PCB['state'] = 1
            #             self.process_queue.put(create_process)
            #             self.create_process_queue.remove(create_process)
            #     else:
            #         create_process.PCB['state'] = 1
            #         self.process_queue.put(create_process)
            #         self.create_process_queue.remove(create_process)

        # 查看阻塞队列中的进程是否有可以进入就绪队列的
        for block_process in self.block_process_queue:
            self.check_resource(block_process,2)
            # if block_process.special_resource[0] == 1:
            #     if (block_process.event == 1 and len(self.buffer) < self.buffer_size and self.mutex == 1) or (block_process.event == 2 and len(self.buffer) > 0 and self.mutex ==1):
            #         block_process_time = block_process.PCB['total_work_time'] - block_process.PCB['work_time']
            #         if block_process_time in block_process.PCB['resource']:
            #             if self.banker_algorithm(block_process, block_process.PCB['resource'][block_process_time]):
            #                 block_process.PCB['state'] = 1
            #                 self.process_queue.put(block_process)
            #                 self.create_process_queue.remove(block_process)
            #         else:
            #             block_process.PCB['state'] = 1
            #             self.process_queue.put(block_process)
            #             self.create_process_queue.remove(block_process)
            # else:
            #     block_process.PCB['state'] = 1
            #     self.process_queue.put(block_process)
            #     self.create_process_queue.remove(block_process)
    def update_queue_info(self):
        # 更新当前进程队列状态
        print_process_queue_dict = []
        if len(self.create_process_queue) == 0:
            print_process_queue_dict.append("创建态进程队列为空")
        else:
            print_process_queue_dict.append("创建态进程队列如下")
            for process in self.create_process_queue:
                print_process_queue_dict.append(
                    "进程" + process.PCB['name'] + " 需要使用处理机的时间为:" + str(process.PCB['work_time']) + "优先级为:" + str(
                        process.PCB['priority']) + "处于的状态是:" + self.process_state_table[process.PCB['state']])
        if len(self.process_queue.queue) == 0:
            print_process_queue_dict.append("就绪进程队列为空")
        else:
            print_process_queue_dict.append("就绪进程队列如下")
            for process in self.process_queue.queue:
                print_process_queue_dict.append(
                    "进程" + process.PCB['name'] + " 需要使用处理机的时间为:" + str(process.PCB['work_time']) + "优先级为:" + str(
                        process.PCB['priority']) + "处于的状态是:" + self.process_state_table[process.PCB['state']])
        if len(self.block_process_queue) == 0:
            print_process_queue_dict.append("阻塞态进程队列为空")
        else:
            print_process_queue_dict.append("阻塞态进程队列如下")
            for process in self.block_process_queue:
                print_process_queue_dict.append(
                    "进程" + process.PCB['name'] + " 需要使用处理机的时间为:" + str(process.PCB['work_time']) + "优先级为:" + str(
                        process.PCB['priority']) + "处于的状态是:" + self.process_state_table[process.PCB['state']])
        if len(self.terminated_process_queue) == 0:
            print_process_queue_dict.append("终止态进程队列为空")
        else:
            print_process_queue_dict.append("终止态进程队列如下")
            for process in self.terminated_process_queue:
                print_process_queue_dict.append(
                    "进程" + process.PCB['name'] + " 需要使用处理机的时间为:" + str(process.PCB['work_time']) + "优先级为:" + str(
                        process.PCB['priority']) + "处于的状态是:" + self.process_state_table[process.PCB['state']])
        if self.cpu.process_in_cpu == None:
            print_process_queue_dict.append("现在无正在上机的进程")
        else:
            if self.cpu.process_in_cpu.use_buffer == 1:
                print_process_queue_dict.append("现在正在上机的进程为" + self.cpu.process_in_cpu.PCB['name'] + "该进程正在使用缓冲区")
            else:
                print_process_queue_dict.append("现在正在上机的进程为" + self.cpu.process_in_cpu.PCB['name'])
        self.print_process_queue = print_process_queue_dict

    def os_run_with_time_slice(self):
        # 时间片用完退出处理机的情况
        if self.cpu.time_slice_used == self.cpu.time_slice:
            self.cpu.time_slice_used = 0
            self.os_time -= 1
            # 判断当前上机进程是否执行完毕，若没有完成，还需再次入队
            if self.cpu.process_in_cpu.PCB['work_time'] > 0:
                self.check_resource(process=self.cpu.process_in_cpu, queue_flag=3)
            #     process_in_cpu_time = self.cpu.process_in_cpu.PCB['total_work_time'] - self.cpu.process_in_cpu.PCB[
            #         'work_time']
            #     if process_in_cpu_time in self.cpu.process_in_cpu.PCB['resource']:
            #         if self.banker_algorithm(self.cpu.process_in_cpu,
            #                                  self.cpu.process_in_cpu.PCB['resource'][process_in_cpu_time]):
            #             self.cpu.process_in_cpu.PCB['state'] = 1
            #             self.process_queue.put(self.cpu.process_in_cpu)
            #             self.cpu.process_in_cpu = None
            #         else:
            #             self.cpu.process_in_cpu.PCB['state'] = 3
            #             self.block_process_queue.append(self.cpu.process_in_cpu)
            #             self.cpu.process_in_cpu = None
            #     else:
            #         self.cpu.process_in_cpu.PCB['state'] = 1
            #         self.process_queue.put(self.cpu.process_in_cpu)
            #         self.cpu.process_in_cpu = None
            else:
                self.return_buffer()
                self.cpu.process_in_cpu.PCB['state'] = 4
                self.terminated_process_queue.append(self.cpu.process_in_cpu)
                self.return_resource(self.cpu.process_in_cpu)
                self.cpu.process_in_cpu = None

        # 时间片未用完退出处理机的情况
        else:
            if self.cpu.process_in_cpu != None:
                self.return_buffer()
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
                self.os_time = self.cpu.run_with_time_slice()

    def os_run_with_static_priority(self):
        if self.cpu.process_in_cpu != None:
            self.return_buffer()
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
            self.os_time = self.cpu.run_with_static_priority()

    def run(self):
        while True:
            self.check_process_to_queue()
            self.update_queue_info()
            # 根据进程调度方式来执行对应代码
            if self.process_scheduling_algorithm == 0:
                self.os_run_with_time_slice()
            elif self.process_scheduling_algorithm == 1:
                self.os_run_with_static_priority()
            self.os_time += 1
            time.sleep(1)