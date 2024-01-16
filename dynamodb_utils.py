from logger_config import setup_logger
import boto3
from decimal import Decimal
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Attr
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

# 常量定义
DYNAMODB_TABLE_NAME = 'SGD_EXCHANGE_RATE'  # 日志文件相对目录

logger = setup_logger(__name__)

def write_to_dynamodb(rate):
    # 创建 DynamoDB 资源
    logger.info("正在创建DynamoDB资源...")
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)

    # 准备数据
    data = {
        'Date': datetime.now().strftime('%Y-%m-%d'),
        'Time': datetime.now().strftime('%H:%M:%S'),
        'Rate': Decimal(str(rate))
    }

    # 写入数据
    logger.info("正在写入DynamoDB...")
    table.put_item(Item=data)
    logger.info("已写入DynamoDB")
    
def query_and_plot():
    # 初始化DynamoDB客户端
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    
    # 计算查询的开始日期
    start_date = datetime.now() - timedelta(days=1)
    start_date_str = start_date.strftime('%Y-%m-%d')  # DynamoDB需要的日期格式
    print(start_date_str)
    
    # 查询最近2天的数据
    response = table.scan(
        FilterExpression=Attr('Date').gte(start_date_str)
    )
    
    # 提取日期、时间和汇率（每隔一个元素取一个元素，从而将数据量减少一半）
    dates = [item['Date'] for i, item in enumerate(response['Items']) if i % 2 == 0]
    times = [item['Time'] for i, item in enumerate(response['Items']) if i % 2 == 0]
    rates = [float(item['Rate']) for i, item in enumerate(response['Items']) if i % 2 == 0]
    
    # 合并日期和时间为完整的datetime对象
    datetimes = [datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S") for date, time in zip(dates, times)]
    
    # 绘制曲线图
    plt.figure(figsize=(16, 8))
    plt.plot(datetimes, rates, '-o', color='darkblue', markersize=2, linewidth=1.5, alpha=0.7, label='SGD Rate')
    plt.title('SGD Exchange Rate Over the Past 2 Days', fontsize=20, pad=20)

    # 设置日期格式
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=3))

    # 自动旋转日期标记以避免重叠
    plt.gcf().autofmt_xdate()

    # 标记最高值、最低值和平均值
    max_rate = max(rates)
    min_rate = min(rates)
    avg_rate = round(sum(rates) / len(rates), 2)

    max_index = rates.index(max_rate)
    min_index = rates.index(min_rate)
    avg_index = rates.index(min(rates, key=lambda x:abs(x-avg_rate))) # 找到最接近平均值的点
    
    # 绘制最大值和最小值的点
    plt.plot(datetimes[max_index], max_rate, 'ro', markersize=5)
    plt.plot(datetimes[min_index], min_rate, 'go', markersize=5)
    
    # 添加最高值、最低值和平均值的点标签
    plt.annotate(f'Max: {max_rate} at {datetimes[max_index]}', xy=(datetimes[max_index], max_rate), xytext=(datetimes[max_index], max_rate + 0.05),
                 ha='center', va='bottom', color='red', fontsize=17)
    plt.annotate(f'Min: {min_rate} at {datetimes[min_index]}', xy=(datetimes[min_index], min_rate), xytext=(datetimes[min_index], min_rate - 0.05),
                 ha='center', va='top', color='green', fontsize=17)
    plt.annotate(f'Avg: {avg_rate}', xy=(datetimes[avg_index], avg_rate), xytext=(datetimes[-1], avg_rate + 0.05),
                 ha='center', va='bottom', color='grey', fontsize=17)

    plt.axhline(y=max_rate, color='red', linestyle='--', linewidth=1)
    plt.axhline(y=min_rate, color='green', linestyle='--', linewidth=1)
    plt.axhline(y=avg_rate, color='grey', linestyle='--', linewidth=1)

    # 添加网格线
    plt.grid(True)

    # 保存图表
    plt.savefig('exchange_rate_plot.png')
    
if __name__ == '__main__':
    query_and_plot()