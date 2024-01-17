from dotenv import load_dotenv
import os

class Config:
    def __init__(self):
        # 加载环境变量
        load_dotenv()
        # 常量定义与初始化
        self.__constants = {
            'SENDER_EMAIL': os.getenv('SENDER_EMAIL'),    #邮件发送者
            'PASSWORD': os.getenv('PASSWORD'),    #邮箱密码或授权码
            'SMTP_SERVER': os.getenv('SMTP_SERVER'),  #SMTP服务器地址
            'SMTP_PORT': int(os.getenv('SMTP_PORT')),  #SMTP服务器端口
            'PLOT_PATH': os.getenv('PLOT_PATH'),  #绘制图片路径
        }
        # 变量定义（邮件接收者，汇率阈值，连续未找到数据的阈值，查询间隔）
        self.__variables = ['RECEIVER_EMAIL', 'RATE_THRESHOLD', 'MISSING_DATA_THRESHOLD', 'QUERY_INTERVAL']

    def update_parameter(self, name, value):
        if name in self.__variables:
            os.environ[name] = str(value)
        else:
            raise ValueError(f"非法参数名: {name}")

    def get_parameter(self, name):
        # 如果是常量，直接从类属性中获取
        if name in self.__constants:
            return self.__constants[name]
        # 如果是变量，从环境变量中获取
        elif name in self.__variables:
            # 重新加载环境变量
            load_dotenv(override=True)
            return os.getenv(name)
        else:
            raise ValueError(f"非法参数名: {name}")