from utils import plot_utils, dynamodb_utils

if __name__ == "__main__":
    # 查询最近两天的数据
    data = dynamodb_utils.query_recent_days_data(2)
    # 绘制折线图
    plot_utils.plot_recent_days_data(data, 2, 2, "temp/exchange_rate_plot.png")