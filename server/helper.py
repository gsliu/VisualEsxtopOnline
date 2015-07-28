import re

def is_cpu_process_time(item):
    #\\proma-2n-dhcp60.eng.vmware.com\Physical Cpu(0)\% Processor Time
    pattern = re.compile(r'.*Physical Cpu\([0-9]+\)\\.*Processor Time.*')
    match = pattern.match(item)
    if match:
        return True
    return False


def is_cpu_util_time(item):
    #\\proma-2n-dhcp60.eng.vmware.com\Physical Cpu(0)\% Util Time
    pattern = re.compile(r'.*Physical Cpu\([0-9]+\)\\.*Util Time.*')
    match = pattern.match(item)
    if match:
        return True
    return False


def is_memory_kernel_mbytes(item):
    #\\proma-2n-dhcp60.eng.vmware.com\Memory\Kernel MBytes
    pattern = re.compile(r'.*Memory\\Kernel MBytes.*')
    match = pattern.match(item)
    if match:
        return True
    return False


def is_memory_nonkernel_mbytes(item):
    #\\proma-2n-dhcp60.eng.vmware.com\Memory\NonKernel MBytes,
    pattern = re.compile(r'.*Memory\\NonKernel MBytes.*')
    match = pattern.match(item)
    if match:
        return True
    return False


def is_memory_kernel_state(item):
    #\\proma-2n-dhcp60.eng.vmware.com\Memory\Kernel State,
    pattern = re.compile(r'.*Memory\\Kernel State.*')
    match = pattern.match(item)
    if match:
        return True
    return False


def is_memory_pshare_shared_mbytes(item):
    #\\proma-2n-dhcp60.eng.vmware.com\Memory\PShare Shared MBytes,
    pattern = re.compile(r'.*Memory\\PShare Shared MBytes.*')
    match = pattern.match(item)
    if match:
        return True
    return False


def is_memory_swap_target_mbytes(item):
    #\\proma-2n-dhcp60.eng.vmware.com\Memory\Swap Target MBytes,
    pattern = re.compile(r'.*Memory\\Swap Target MBytes.*')
    match = pattern.match(item)
    if match:
        return True
    return False


def is_memory_swap_mbytes_read_sec(item):
    #\\proma-2n-dhcp60.eng.vmware.com\Memory\Swap MBytes Read/sec,
    pattern = re.compile(r'.*Memory\\Swap MBytes Read/sec.*')
    match = pattern.match(item)
    if match:
        return True
    return False


def is_memory_swap_mbytes_write_sec(item):
    #\\proma-2n-dhcp60.eng.vmware.com\Memory\Swap MBytes Write/sec
    pattern = re.compile(r'.*Memory\\Swap MBytes Write/sec.*')
    match = pattern.match(item)
    if match:
        return True
    return False