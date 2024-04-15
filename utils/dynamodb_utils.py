import boto3
from decimal import Decimal
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Key
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
    
    # 计算待查询日期
    today = datetime.now()
    dates_to_query = [today - timedelta(days=i) for i in range(day_interval)]


    # 查询数据
    logger.info(f"正在查询最近{day_interval}天的数据...")
    results = []
    for query_date in dates_to_query:
        date_str = query_date.strftime('%Y-%m-%d')
        response = table.query(
            KeyConditionExpression=Key('Date').eq(date_str)
        )
        if response['Items']:
            results.extend(response['Items'])
        
    if len(results) == 0:
        logger.error("未找到任何数据！")
        return None

    logger.info(f"已查询到{len(results)}条数据...")
    
    # 拆分数据
    dates = [item['Date'] for item in results]
    times = [item['Time'] for item in results]
    rates = [float(item['Rate']) for item in results]
    
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
    print(query_recent_days_data())