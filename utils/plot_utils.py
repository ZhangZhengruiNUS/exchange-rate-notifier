from datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from decorators import timeit, resources_debug_monitor
import matplotlib.patheffects as path_effects
from logger_config import get_global_logger

# 获取全局日志对象
logger = get_global_logger()

@timeit
@resources_debug_monitor
def plot_recent_data(data, day_interval=2, thin_factor=2, path="exchange_rate_plot.png"):
    # 校验数据
    if not data:
        logger.error("无可用数据来绘制图表！")
        return False
    logger.info(f"接收到{len(data)}条数据")
    
    # 拆分并稀释数据
    datetimes = [item[0] for i, item in enumerate(data) if i % thin_factor == 0]
    rates = [item[1] for i, item in enumerate(data) if i % thin_factor == 0]
    logger.info(f"稀释数据后，剩余数据量为{len(rates)}，稀释系数为{thin_factor}")

    # 开始绘图
    logger.info("正在绘制图表...")
    plt.figure(figsize=(16, 7))
    plt.plot(datetimes, rates, '-o', color='darkblue', markersize=2, linewidth=1.5, alpha=0.7, label='SGD Rate')
    plt.title(f"SGD Exchange Rate Over the Past {day_interval} Days", fontsize=20, pad=25, weight='bold')

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
    
    # 添加带阴影的标签
    def annotate_with_shadow(text, xy, xytext, ha, va, color, fontsize, weight):
        annotation = plt.annotate(text, xy=xy, xytext=xytext, ha=ha, va=va, color=color, fontsize=fontsize, weight=weight)
        annotation.set_path_effects([path_effects.PathPatchEffect(offset=(0.3, -0.3), hatch=None, facecolor='darkgray'),
                                    path_effects.Normal()])
        return annotation

    # 添加最高值、最低值、平均值和最新值的点标签
    annotate_with_shadow(f'Max: {max_rate} at {datetimes[max_index]}', xy=(datetimes[max_index], max_rate), xytext=(datetimes[max_index], max_rate + 0.03),
                        ha='center', va='bottom', color='red', fontsize=16, weight='bold')
    annotate_with_shadow(f'Min: {min_rate} at {datetimes[min_index]}', xy=(datetimes[min_index], min_rate), xytext=(datetimes[min_index], min_rate - 0.03),
                        ha='center', va='top', color='green', fontsize=16, weight='bold')
    annotate_with_shadow(f'Avg: {avg_rate}', xy=(datetimes[avg_index], avg_rate), xytext=(datetimes[-1] + timedelta(hours=2.6), avg_rate - 0.03),
                        ha='center', va='bottom', color='grey', fontsize=16, weight='bold')
    annotate_with_shadow(f'Latest: {rates[-1]}', xy=(datetimes[-1], rates[-1]), xytext=(datetimes[-1] + timedelta(hours=0.3), rates[-1] + 0.1),
                        ha='left', va='top', color='orange', fontsize=16, weight='bold')

    # 调整图的边界
    plt.subplots_adjust(left=0.12, right=0.88, top=0.87, bottom=0.16)
    
    # 绘制与Y轴相连的水平线
    plt.axhline(y=max_rate, color='red', linestyle='--', linewidth=1)
    plt.axhline(y=min_rate, color='green', linestyle='--', linewidth=1)
    plt.axhline(y=avg_rate, color='grey', linestyle='--', linewidth=1)

    # 添加文字到图片的右下角
    plt.gcf().text(0.990, 0.02, 'Data update time: ' + str(datetimes[-1]),
         fontsize=12, ha='right', va='bottom', color='#505050', weight='bold')
    
    # 添加网格线
    plt.grid(True)
    
    # 保存图表
    plt.savefig(path, dpi=150)
    plt.close()  #关闭图形，否则会留在内存里
    logger.info("已绘制完成")
    
    return True