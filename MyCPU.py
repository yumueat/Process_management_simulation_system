# -*- coding: utf-8 -*-
"""
@author yumu
@className MyCPU
@version 1.0.0
@describe TODO
"""
import threading
import time

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
    def run_with_time_slice(self):
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
            # 减少1秒上机进程所需的时间
            self.process_in_cpu.PCB['work_time'] -= 1
            self.cpu_log.append(str(self.os_time)+"时刻" + self.process_in_cpu.PCB['name'] + "已上cpu工作1秒")
            self.time_slice_used +=1
            self.os_time +=1
            time.sleep(1)

    # 非抢占式静态优先级调度
    def run_with_static_priority(self):
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