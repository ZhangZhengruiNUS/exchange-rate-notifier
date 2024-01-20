import time
from functools import wraps
from utils import common_utils
from logger_config import get_global_logger

# 获取全局日志对象
logger = get_global_logger()

def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()  # 获取开始时间
        result = func(*args, **kwargs)
        end_time = time.time()  # 获取结束时间
        exec_time = end_time - start_time  # 计算执行时间，单位为秒

        logger.info(f"{func.__name__}函数的执行时间为：{exec_time:.3f} seconds")
        return result
    
    return wrapper

def resources_debug_monitor(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        common_utils.log_process_resources(f"{func.__name__}函数执行前", "debug")
        result = func(*args, **kwargs)
        common_utils.log_process_resources(f"{func.__name__}函数执行后", "debug")
        return result

    return wrapper