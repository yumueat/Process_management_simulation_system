# -*- coding: utf-8 -*-
"""
@author yumu
@className MyCPU
@version 1.0.0
@describe TODO
"""
import threading
import time
from MyProcess import *
'''
    cpu类
    process_in_cpu 当前上机运行的进程
    flag 标志位
    cpu_log cpu记录，用于存储进程上机情况
    os_time 系统时间
    time_slice 时间片
    time_slice_used 已经使用的时间片
'''

class MyCPU:
    process_in_cpu = None
    flag = 0
    cpu_log = []
    os_time = None
    time_slice = None
    time_slice_used = 0

    # 时间片轮转法
    def run_with_time_slice(self,os):
        while True:
            # 标志位为1或当前上机进程所需工作时间为0或时间片用完时，该进程放弃处理机
            if self.flag == 1:
                return self.os_time - 1
            if self.process_in_cpu.PCB['work_time'] == 0:
                self.process_in_cpu.PCB['state'] = 4
                return self.os_time - 1
            if self.time_slice_used == self.time_slice:
                self.process_in_cpu.PCB['state'] = 1
                return self.os_time - 1
            #进程的具体工作内容
            process_time = self.process_in_cpu.PCB['total_work_time'] - self.process_in_cpu.PCB['work_time']
            # 进程通信
            for message_send in self.process_in_cpu.message_send:
                if process_time == message_send[0]:
                    os.message_passing(process=message_send[1],message=message_send[2])
                    self.cpu_log.append(str(self.os_time) + "时刻" + self.process_in_cpu.PCB['name'] + "发送信息" +message_send[2] )

            # 进程外存访问
            for file_access in self.process_in_cpu.file_access:
                if process_time == file_access[0]:
                    os.external_memory_access(file_access=file_access)

            # 线程创建
            for thread_create in self.process_in_cpu.thread_create_list:
                if process_time == thread_create[0]:
                    temp_process = MyProcess(name=thread_create[1],work_time=thread_create[2],priority=self.process_in_cpu.PCB['priority'],resource={},event=[],special_resource=[0,{}],thread_flag=1)
                    temp_process.set_page_access_list(page_access_list=[], page_number=0)
                    temp_process.main_process = self.process_in_cpu
                    self.process_in_cpu.thread_table.append(temp_process)
                    os.create_process_queue.append(temp_process)

            # 请求访问一页
            for page_access in  self.process_in_cpu.page_access_list:
                if process_time == page_access[0]:
                    os.page_table_request_mechanism(page_access)

            # 减少1秒上机进程所需的时间
            self.process_in_cpu.PCB['work_time'] -= 1
            self.cpu_log.append(str(self.os_time)+"时刻" + self.process_in_cpu.PCB['name'] + "已上cpu工作1秒")
            self.time_slice_used +=1
            self.os_time +=1
            time.sleep(1)

    # 非抢占式静态优先级调度
    def run_with_static_priority(self,os):
        while True:
            # 标志位为1或当前上机进程所需工作时间为0时，该进程放弃处理机
            if self.flag == 1:
                return self.os_time - 1
            if self.process_in_cpu.PCB['work_time'] == 0:
                self.process_in_cpu.PCB['state'] = 4
                return self.os_time - 1
            # 减少1秒上机进程所需的时间
            self.process_in_cpu.PCB['work_time'] -= 1
            self.cpu_log.append(str(self.os_time)+"时刻" + self.process_in_cpu.PCB['name'] + "已上cpu工作1秒")
            self.os_time +=1
            time.sleep(1)
