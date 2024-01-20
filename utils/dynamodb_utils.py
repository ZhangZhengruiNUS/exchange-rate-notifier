import boto3
from decimal import Decimal
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Attr
from decorators import timeit, resources_debug_monitor
from logger_config import get_global_logger

# 获取全局日志对象
logger = get_global_logger()

# 常量定义
DYNAMODB_TABLE_NAME = 'SGD_EXCHANGE_RATE'  # 日志文件相对目录

@timeit
@resources_debug_monitor
def write_to_dynamodb(rate):
    # 创建 DynamoDB 资源
    table = create_dynamodb_resource()

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

@timeit
@resources_debug_monitor
def query_recent_days_data(day_interval=2):
    # 创建 DynamoDB 资源
    table = create_dynamodb_resource()
    
    # 计算起始日期
    start_date = datetime.now() - timedelta(days=(day_interval-1))
    start_date_str = start_date.strftime('%Y-%m-%d')

    # 查询数据
    logger.info(f"正在查询最近{day_interval}天的数据...")
    response = table.scan(FilterExpression=Attr('Date').gte(start_date_str))

    if not response['Items']:
        logger.error("未找到数据！")
        return None
    logger.info(f"已查询到{len(response['Items'])}条数据...")
    
    # 拆分数据
    dates = [item['Date'] for item in response['Items']]
    times = [item['Time'] for item in response['Items']]
    rates = [float(item['Rate']) for item in response['Items']]
    
    # 排序以及合并数据
    data = sorted([(datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S"), rate) for date, time, rate in zip(dates, times, rates)])
    
    return data

def create_dynamodb_resource():
    logger.info("正在创建DynamoDB资源...")
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    logger.info("已创建DynamoDB资源")
    return table
    
if __name__ == '__main__':
    query_recent_days_data()