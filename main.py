import time
from rate_fetcher import get_sgd_rate
import utils

def main():
    print("[" + utils.get_current_time() + "] 汇率通知器开始启动...")
    # 加载基础参数
    config = utils.load_config()

    # 主循环
    nfound_count = 0  # 连续未找到数据计数
    try:
        while True:
            # 获取最新汇率
            found, current_rate = get_sgd_rate()
            
            # 判断是否找到数据
            if found:
                nfound_count = 0
                # 判断是否低于阈值
                if current_rate < config["rate_threshold"]:
                    utils.send_email("新加坡汇率通知",
                                    f"当前SGD汇率为{current_rate}，低于设定阈值{config['rate_threshold']}，可以考虑购汇！",
                                    config)
            else:
                nfound_count += 1
                # 判断未找到数据次数是否大于阈值
                if nfound_count > config["missing_data_threshold"]:
                    utils.send_email("汇率通知器报警",
                                    f"已超过设定阈值{config['missing_data_threshold']}次未找到数据，请检查服务器网络状况或网页结构是否发生变化！",
                                    config)
                    print("[" + utils.get_current_time() + "] 汇率通知器已自动停止")
                    break
            
            # 查询间隔
            time.sleep(config['query_interval'])
    except KeyboardInterrupt:
        print("[" + utils.get_current_time() + "] 汇率通知器已手动停止")

if __name__ == '__main__':
    main()