from datetime import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
import os
from dotenv import load_dotenv

# 常量定义
LOG_DIR = 'logs'  # 日志文件相对目录
LOG_FILE_PREFIX = "app"  # 日志文件前缀

def setup_logger(logger_name):
    # 如果已经创建过logger，直接返回
    if logger_name in logging.root.manager.loggerDict:
        return logging.getLogger(logger_name)
    
    # 创建日志文件路径
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    log_file_path = custom_log_file_path()

    # 创建TimedRotatingFileHandler
    file_handler = TimedRotatingFileHandler(log_file_path,
                                            when="midnight",
                                            interval=1, # 每天轮换一次
                                            backupCount=7)  # 保留7天
    formatter = logging.Formatter('[%(asctime)s.%(msecs)03d][%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')  #设置日志格式
    file_handler.setFormatter(formatter)
    file_handler.suffix = "%Y-%m-%d"
    file_handler.namer = custom_log_file_path

    # 创建logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    
    # 添加处理器
    logger.addHandler(file_handler)  # 添加文件日志处理器
    load_dotenv()
    if not os.getenv('ENV_TYPE', '').lower() == 'production':  # 生产环境不添加控制台日志处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

def custom_log_file_path(name=None):
    return LOG_DIR + "/" + LOG_FILE_PREFIX + "_" + datetime.now().strftime("%Y-%m-%d") + '.log'

if __name__ == "__main__":
    logger = setup_logger(__name__)
    logger.info("这是一条普通日志")
    logger.error("这是一条报错日志")