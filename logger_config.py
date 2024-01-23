from datetime import datetime, timedelta
import logging
from logging.handlers import TimedRotatingFileHandler
import os
from dotenv import load_dotenv

# 常量定义
LOG_DIR = 'logs'  # 日志文件相对目录
LOG_FILE_PREFIX = "app"  # 日志文件前缀

def custom_log_file_path(name=None, initial=False):
    if initial:
        # 当日记录的日志文件的路径
        return LOG_DIR + "/" + LOG_FILE_PREFIX + "_today" + '.log'
    else:
        # 轮换时的前一天日志文件的路径
        return LOG_DIR + "/" + LOG_FILE_PREFIX + "_" + (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d") + '.log'

def setup_global_logger():
    # 创建日志文件路径
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    initial_log_file_path = custom_log_file_path(initial=True)

    # 创建TimedRotatingFileHandler
    file_handler = TimedRotatingFileHandler(
        initial_log_file_path,  # 初始日志文件路径
        when="midnight", # 每天午夜轮换
        interval=1, # 每天轮换一次
        backupCount=7, # 保留7天
        encoding='utf-8'
    )
    formatter = logging.Formatter('[%(asctime)s.%(msecs)03d][%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)  #设置日志格式
    file_handler.namer = custom_log_file_path  # 文件轮换时的命名函数
    
    # 加载环境变量
    load_dotenv()

    # 设置全局日志级别
    log_level = logging.DEBUG if os.getenv('LOG_LEVEL', '').lower() == 'debug' else logging.INFO
    logging.basicConfig(level=log_level, handlers=[file_handler])

    # 生产环境中不添加控制台日志处理器
    if not os.getenv('ENV_TYPE', '').lower() == 'production':
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logging.getLogger().addHandler(console_handler)
        
    logger = logging.getLogger(__name__)
    logger.info(f"已创建全局日志记录器{__name__} 日志文件夹路径为{LOG_DIR}")

def get_global_logger():
    # 检查是否已经有日志配置，如果没有，进行基本配置
    if not logging.getLogger().hasHandlers():
        setup_global_logger()
    return logging.getLogger(__name__)

if __name__ == "__main__":
    pass