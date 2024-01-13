import time
from functools import wraps
from logger_config import setup_logger

logger = setup_logger(__name__)

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

        logger.info(f"{func.__name__}函数的执行时间为：{int(hours)}时{int(minutes)}分{int(seconds)}秒")

        return result

    return wrapper