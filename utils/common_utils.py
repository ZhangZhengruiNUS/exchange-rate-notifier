from datetime import timedelta
import os
from dotenv import load_dotenv
from logger_config import setup_logger
import psutil
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

logger = setup_logger(__name__)

def log_process_resources():
    # 获取当前进程ID
    pid = os.getpid()
    
    # 使用psutil获取进程对象
    current_process = psutil.Process(pid)

    # 获取CPU和内存使用信息
    cpu_usage = current_process.cpu_percent(interval=1.0)  # 可以指定检测间隔
    memory_usage = current_process.memory_percent()  # 内存使用百分比

    # 记录日志
    logger.info(f"当前进程[{pid}]的CPU使用率: {cpu_usage:.2f}% 内存使用率: {memory_usage:.2f}%")
    
def plot_data(data, day_interval=2, path="exchange_rate_plot.png"):
    # 校验数据
    if not data:
        logger.error("无可用数据来绘制图表！")
        return False
    logger.info(f"接收到{len(data[0])}条数据，开始绘图...")

    # 拆分数据
    datetimes = [item[0] for item in data]
    rates = [item[1] for item in data]

    # 开始绘图
    plt.figure(figsize=(16, 8))
    plt.plot(datetimes, rates, '-o', color='darkblue', markersize=2, linewidth=1.5, alpha=0.7, label='SGD Rate')
    plt.title(f"SGD Exchange Rate Over the Past {day_interval} Days", fontsize=20, pad=20)

    # 设置日期格式
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=3))

    # 自动旋转日期标记以避免重叠
    plt.gcf().autofmt_xdate(rotation=15)

    # 找出最高值、最低值和平均值
    max_rate = max(rates)
    min_rate = min(rates)
    avg_rate = round(sum(rates) / len(rates), 2)

    max_index = rates.index(max_rate)
    min_index = rates.index(min_rate)
    avg_index = rates.index(min(rates, key=lambda x:abs(x-avg_rate))) # 找到最接近平均值的点
    
    # 绘制最大值、最小值和最新值的点
    plt.scatter(datetimes[max_index], max_rate, color='red', s=40)
    plt.scatter(datetimes[min_index], min_rate, color='green', s=40)
    plt.scatter(datetimes[-1], rates[-1], color='blue', s=40)
    
    # 添加最高值、最低值、平均值和最新值的点标签
    plt.annotate(f'Max: {max_rate} at {datetimes[max_index]}', xy=(datetimes[max_index], max_rate), xytext=(datetimes[max_index], max_rate + 0.05),
                 ha='center', va='bottom', color='red', fontsize=16)
    plt.annotate(f'Min: {min_rate} at {datetimes[min_index]}', xy=(datetimes[min_index], min_rate), xytext=(datetimes[min_index], min_rate - 0.05),
                 ha='center', va='top', color='green', fontsize=16)
    plt.annotate(f'Avg: {avg_rate}', xy=(datetimes[avg_index], avg_rate), xytext=(datetimes[-1], avg_rate + 0.05),
                 ha='center', va='bottom', color='grey', fontsize=16)
    plt.annotate(f'Latest: {rates[-1]}', xy=(datetimes[-1], rates[-1]), xytext=(datetimes[-1] + timedelta(hours=0.3), rates[-1] + 0.05),
                 ha='left', va='top', color='orange', fontsize=16)

    # 绘制与Y轴相连的水平线
    plt.axhline(y=max_rate, color='red', linestyle='--', linewidth=1)
    plt.axhline(y=min_rate, color='green', linestyle='--', linewidth=1)
    plt.axhline(y=avg_rate, color='grey', linestyle='--', linewidth=1)

    # 添加网格线
    plt.grid(True)

    # 保存图表
    plt.savefig(path, dpi=150)
    logger.info("已绘制完成")
    
    return True
    
def delete_file(path):
    if os.path.isfile(path):
        os.remove(path)