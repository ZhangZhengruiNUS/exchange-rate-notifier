import time
from functools import wraps
import utils

def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time

        # 将执行时间转换为小时、分钟和秒
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)

        print("[{}] {}函数的执行时间为：{}时{}分{}秒".format(utils.get_current_time(), func.__name__, int(hours), int(minutes), int(seconds)))

        return result

    return wrapper