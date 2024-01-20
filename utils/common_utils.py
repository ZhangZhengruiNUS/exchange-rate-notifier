import os
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