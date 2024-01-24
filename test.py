from utils import plot_utils, dynamodb_utils

if __name__ == "__main__":
    query_days_str = input("查询天数：")
    query_days = int(query_days_str)
    # 查询最近两天的数据
    data = dynamodb_utils.query_recent_days_data(query_days)
    # 绘制折线图
    plot_utils.plot_recent_days_data(data, query_days, query_days, query_days + 1, "temp/exchange_rate_plot.png", is_show=True)