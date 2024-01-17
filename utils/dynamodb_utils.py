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

def query_recent_days_data(day_interval=2):
    logger.info("正在创建DynamoDB资源...")
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)

    start_date = datetime.now() - timedelta(days=(day_interval-1))
    start_date_str = start_date.strftime('%Y-%m-%d')

    logger.info(f"正在查询最近{day_interval}天的数据...")
    response = table.scan(FilterExpression=Attr('Date').gte(start_date_str))

    if not response['Items']:
        logger.error("未找到数据！")
        return None

    dates = [item['Date'] for i, item in enumerate(response['Items']) if i % 2 == 0]
    times = [item['Time'] for i, item in enumerate(response['Items']) if i % 2 == 0]
    rates = [float(item['Rate']) for i, item in enumerate(response['Items']) if i % 2 == 0]

    data = sorted([(datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S"), rate) for date, time, rate in zip(dates, times, rates)])
    return data
    
if __name__ == '__main__':
    query_recent_days_data()