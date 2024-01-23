from logger_config import setup_global_logger
# 初始化全局日志对象
setup_global_logger()

import logging
import time
from rate_fetcher import get_sgd_rate
from utils import common_utils, dynamodb_utils, email_utils, plot_utils
from config import Config

def main():
    logger = logging.getLogger(__name__)
    logger.info("-----汇率通知器开始启动-----")

    # 基础变量定义
    nfound_count = 0  # 连续未找到数据计数
    
    # 创建基础参数Config对象
    config = Config()

    # 主循环
    try:
        while True:
            common_utils.log_process_resources("开始新的循环", "info")
            # 获取最新汇率
            found, current_rate = get_sgd_rate()
            # 判断是否找到数据
            if found:
                nfound_count = 0  # 重置连续未找到数据计数
                # 写入数据库
                dynamodb_utils.write_to_dynamodb(current_rate)
                # 判断是否低于阈值
                if current_rate < float(config.get_parameter("RATE_THRESHOLD")):
                    # 查询最近两天的数据
                    data = dynamodb_utils.query_recent_days_data(int(config.get_parameter("PLOT_RECENT_DAYS")))
                    if data is None:
                        email_utils.send_email("汇率通知器报警",
                                        f"汇率通知器未查询到数据库中最近{config.get_parameter('PLOT_RECENT_DAYS')}天的数据，请检查数据库是否正常！",
                                        config)
                        logger.error(f"汇率通知器未查询到数据库中最近{config.get_parameter('PLOT_RECENT_DAYS')}天的数据，已自动终止")
                        break
                    # 绘制折线图
                    if not plot_utils.plot_recent_days_data(data, 
                                                            int(config.get_parameter("PLOT_RECENT_DAYS")), 
                                                            int(config.get_parameter("PLOT_RECENT_DAYS")), 
                                                            int(config.get_parameter("PLOT_RECENT_DAYS")) + 1,
                                                            config.get_parameter("PLOT_PATH")):
                        email_utils.send_email("汇率通知器报警",
                                        f"汇率通知器绘制图表失败，请检查服务器或程序是否正常！",
                                        config)
                        logger.error(f"汇率通知器绘制图表失败，已自动终止")
                        break
                    # 若当前时间在指定时间范围内，则发送邮件
                    if common_utils.check_time_in_range(config.get_parameter("NOTIFY_START_TIME"), config.get_parameter("NOTIFY_END_TIME")):
                        email_utils.send_email("新加坡汇率通知",
                                        f"当前SGD汇率为{current_rate}，低于设定阈值{config.get_parameter('RATE_THRESHOLD')}，可以考虑购汇！",
                                        config, image_path=config.get_parameter("PLOT_PATH"))
            else:
                nfound_count += 1 # 连续未找到数据计数加1
                # 判断未找到数据次数是否大于阈值
                if nfound_count > int(config.get_parameter("MISSING_DATA_THRESHOLD")):
                    email_utils.send_email("汇率通知器报警",
                                    f"已超过设定阈值{config.get_parameter('MISSING_DATA_THRESHOLD')}次未找到数据，请检查服务器网络状况或网页结构是否发生变化！",
                                    config)
                    logger.error(f"汇率通知器由于超过设定阈值{config.get_parameter('MISSING_DATA_THRESHOLD')}次未找到数据，已自动终止")
                    break
            
            # 设置查询间隔
            logger.info(f"正在等待查询间隔{config.get_parameter('QUERY_INTERVAL')}秒...")
            time.sleep(int(config.get_parameter('QUERY_INTERVAL')))
            
    except KeyboardInterrupt:
        # 手动停止
        logger.info("汇率通知器已手动停止")
        
    except Exception as e:
        # 其他异常（发送邮件）
        logger.critical(f"汇率通知器异常终止: {e}", exc_info=True)
        email_utils.send_email("汇率通知器报警",
                            f"主程序由于不知名原因意外停止，请检查服务器运行状况！\n报错信息如下：\n{e}",
                            config)
        
    finally:
        logger.info("-----汇率通知器已终止-----")
            
if __name__ == '__main__':
    main()