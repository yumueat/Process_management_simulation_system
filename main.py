from utils import *
from MyOS import *
from MyProcess import *
from Command import *

if __name__ == '__main__':
    command_exc = Command()
    # os = time_slice_rotation_test(2,5)
    # os = static_priority_scheduling_test(5)
    # os = deadlock_handling_test(2)
    auto_process_mutual_exclusion_test(2)
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