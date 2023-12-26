import time
from rate_fetcher import get_sgd_rate
import utils

def main():
    # 加载基础参数
    config = utils.load_config()

    # 主循环
    try:
        while True:
            # 获取最新汇率
            current_rate = get_sgd_rate()
            
            # 判断是否低于阈值
            if current_rate < config["threshold_rate"]:
                subject = "新加坡汇率通知"
                body = f"当前SGD汇率为{current_rate}，低于设定阈值{config['threshold_rate']}，可以考虑购汇！"
                utils.send_email(subject, body, config)
            
            # 查询间隔
            time.sleep(config['query_interval'])
    except KeyboardInterrupt:
        print("程序已停止")

if __name__ == '__main__':
    main()