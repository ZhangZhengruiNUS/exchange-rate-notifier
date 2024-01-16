import time
from rate_fetcher import get_sgd_rate
import utils
from logger_config import setup_logger
import dynamodb_utils

logger = setup_logger(__name__)

def main():
    logger.info("-----汇率通知器开始启动-----")
    
    # 基础变量定义
    nfound_count = 0  # 连续未找到数据计数
    
    # 加载基础参数
    config = utils.load_config()

    # 主循环
    try:
        while True:
            # 获取最新汇率
            found, current_rate = get_sgd_rate()
            
            # 判断是否找到数据
            if found:
                nfound_count = 0  # 重置连续未找到数据计数
                dynamodb_utils.write_to_dynamodb(current_rate)  # 写入AWS DynamoDB
                if current_rate < config["rate_threshold"]:  # 判断是否低于阈值
                    utils.send_email("新加坡汇率通知",
                                    f"当前SGD汇率为{current_rate}，低于设定阈值{config['rate_threshold']}，可以考虑购汇！",
                                    config)
            else:
                nfound_count += 1 # 连续未找到数据计数加1
                if nfound_count > config["missing_data_threshold"]:  # 判断未找到数据次数是否大于阈值
                    utils.send_email("汇率通知器报警",
                                    f"已超过设定阈值{config['missing_data_threshold']}次未找到数据，请检查服务器网络状况或网页结构是否发生变化！",
                                    config)
                    logger.error(f"汇率通知器由于超过设定阈值{config['missing_data_threshold']}次未找到数据，已自动终止")
                    break
                
            logger.info(f"正在等待查询间隔{config['query_interval']}秒...")
            time.sleep(config['query_interval'])  # 设置查询间隔
            
    except KeyboardInterrupt:
        # 手动停止异常
        logger.info("汇率通知器已手动停止")
        
    except Exception as e:
        # 其他异常（发送邮件）
        logger.critical(f"汇率通知器异常终止: {e}", exc_info=True)
        utils.send_email("汇率通知器报警",
                            f"主程序由于不知名原因意外停止，请检查服务器运行状况！\n报错信息如下：\n{e}",
                            config)
        
    finally:
        logger.info("-----汇率通知器已终止-----")
            
if __name__ == '__main__':
    main()