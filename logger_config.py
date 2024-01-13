from datetime import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
import os

def setup_logger(logger_name):
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file_path = log_dir + '/app_' + datetime.now().strftime("%Y-%m-%d") + '.log'

    # 创建TimedRotatingFileHandler
    file_handler = TimedRotatingFileHandler(log_file_path,
                                            when="midnight",
                                            interval=3,
                                            backupCount=7, # 保留7天
                                            utc=True)
    formatter = logging.Formatter('[%(asctime)s.%(msecs)03d][%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')  #设置日志格式
    file_handler.setFormatter(formatter)
    file_handler.suffix = "%Y-%m-%d"
    file_handler.namer = lambda name: name.replace(".log", "") + "_" + datetime.now().strftime("%Y-%m-%d") + ".log"

    # 创建StreamHandler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    # 添加两个处理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

if __name__ == "__main__":
    logger = setup_logger(__name__)
    logger.info("这是一条普通日志")
    logger.error("这是一条报错日志")