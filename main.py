from utils import *
from MyOS import *
from MyProcess import *
from Command import *

if __name__ == '__main__':
    command_exc = Command()
    # 状态切换和调度可以用同一个用例来测试
    # 自动的时间片轮转法进程调度测试，其中2是时间片长度，5是生成的进程数目
    # 会观察到的现象如下：进程按照入队顺序依次上机执行，时间片到后下机，然后重新入队
    # auto_time_slice_rotation_test(2,5)

    # 自动的静态优先级进程调度测试，5是生成的进程数目
    # auto_static_priority_scheduling_test(5)

    # 自动的进程互斥测试，测试用的进程已经提前写好，其中p0是消费者，p1是生产者，p2是生产者，p3是消费者，p4是消费者
    # 会观察到的现象如下：一开始p0可以访问缓冲区，但是缓冲区中无资源，遂不会进入就绪队列，而p1可以访问缓冲区，也可以进行生产，所以p1进入就绪队列
    # p2由于缓冲区已分配给p1使用，所以p2也不会进入就绪队列，p3p4同理
    # auto_process_mutual_exclusion_test(2)

    # 自动的进程同步测试，测试用的进程已经提前写好，其中p0在3时刻需要p1运行完成后的结果，所以在运行到3时刻后p0会被阻塞
    # auto_process_synchronization_test(2)

    # 自动进程通信测试，会输出进程队列信息，cpu日志以及各个进程的消息列表
    # auto_process_communicate_test(2)

    # 自动死锁处理测试，这里的死锁处理是基于银行家算法的死锁避免，每一次进程请求分配资源系统都会使用银行家算法，生成安全队列，看是否能分配
    # auto_deadlock_handling_test(2)

    # 自动内存分配和回收测试，会输出进程队列情况和内存分配情况
    # auto_memory_allocation_and_recycling_test(2)

    # 自动内存换入换出测试，会输出页表和页面调入调出记录
    # auto_memory_swapping_in_and_out_test(2)

    # 自动外存访问测试，已经提前写好了测试用的进程，其中p0会先向文件中写入内容，然后p1会读取文件内容，再然后p1又会向文件中写入内容，最后p0会读取文件的内容
    # 运行时会输出进程队列信息、cpu日志和进程读取到的文件信息
    # auto_external_memory_access(2)

    # 自动线程测试，进程p0会产生两个内核级线程
    # auto_thread_test(2)

    # 挂起和激活测试
    # suspend_and_wake_up_test(2)

    # auto_comprehensive_test(2)

    # 手动测试
    # os = time_slice_rotation_test(2,5)
    while True:
        command = input()
        if command == "print cpu log":
            command_exc.print_cpu_log(os)
        elif command == "print process queue":
            command_exc.print_process_queue(os)
        elif command == "print os time":
            command_exc.print_os_time(os)
        elif command == "print resource allocation log":
            command_exc.print_resource_allocation_log(os)
        elif command == "suspend":
            process_name = input("输入要挂起的进程名")
            command_exc.suspend(os,process_name=process_name)
        elif command == "activation":
            process_name = input("输入要激活的进程名")
            command_exc.activation(os,process_name=process_name)
        elif command == "print process receive message":
            command_exc.print_process_receive_message(os)
        elif command == "print process read file content":
            command_exc.print_process_read_file_content(os)
        elif command == "print memory use":
            command_exc.print_memory_use(os)
        elif command == "print page table":
            command_exc.print_page_table(os)
        elif command == "print page access log":
            command_exc.print_page_access_log(os)
        elif command == "print buffer":
            command_exc.print_buffer(os)