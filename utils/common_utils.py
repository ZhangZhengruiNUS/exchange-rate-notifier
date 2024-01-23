import os
import time
import psutil
from logger_config import get_global_logger

# 获取全局日志对象
logger = get_global_logger()

def log_process_resources(prompt_info, log_level="info"):
    # 获取当前进程ID
    pid = os.getpid()
    
    # 使用psutil获取进程对象
    current_process = psutil.Process(pid)

    # 获取CPU和内存使用信息
    cpu_usage = current_process.cpu_percent(interval=1.0)  # 可以指定检测间隔
    memory_usage = current_process.memory_percent()  # 内存使用百分比

    # 记录日志
    if log_level == "debug":
        logger.debug(f"<{prompt_info}> 当前进程[{pid}]的CPU使用率: {cpu_usage:.2f}% 内存使用率: {memory_usage:.4f}%")
    else:
        logger.info(f"<{prompt_info}> 当前进程[{pid}]的CPU使用率: {cpu_usage:.2f}% 内存使用率: {memory_usage:.4f}%")

def delete_file(path):
    if os.path.isfile(path):
        os.remove(path)
   
def check_time_in_range(start_time, end_time):
    result = False
    # 获取当前时间
    current_time = time.localtime()
    # 获取当前时间的小时和分钟
    current_hour = current_time.tm_hour
    current_minute = current_time.tm_min
    # 获取开始时间的小时和分钟
    start_hour = int(start_time.split(":")[0])
    start_minute = int(start_time.split(":")[1])
    # 获取结束时间的小时和分钟
    end_hour = int(end_time.split(":")[0])
    end_minute = int(end_time.split(":")[1])
    # 判断当前时间是否在指定时间范围内
    if (current_hour > start_hour and current_hour < end_hour) or \
        (current_hour == start_hour and current_minute >= start_minute) or \
        (current_hour == end_hour and current_minute <= end_minute):
        result = True
    logger.info(f"当前时间{current_hour}:{current_minute}是否在{start_hour}:{start_minute}到{end_hour}:{end_minute}之间: {result}")
    return result