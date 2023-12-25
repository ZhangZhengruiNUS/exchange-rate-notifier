import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sgd_rate_fetcher import get_exchange_rate
from dotenv import load_dotenv
import os

# 加载基础参数
load_dotenv()
sender_email = os.getenv("SENDER_EMAIL") # 邮件发送者
receiver_email = os.getenv("RECEIVER_EMAIL")  # 邮件接收者
password = os.getenv("PASSWORD")  # 邮箱密码或专用密码
smtp_server = os.getenv("SMTP_SERVER")  # SMTP服务器地址
smtp_port = int(os.getenv("SMTP_PORT"))  # SMTP服务器端口（SSL为465，TLS为587）
threshold_rate = float(os.getenv("THRESHOLD_RATE")) # 汇率阈值（低于此值时发送邮件）
query_interval = int(os.getenv("QUERY_INTERVAL"))  # 查询间隔，单位为秒

# 主循环
try:
    while True:
        # 获取最新汇率
        current_rate = get_exchange_rate()
        
        # 判断是否低于阈值
        if current_rate < threshold_rate:
            # 创建邮件对象和邮件消息
            print("正在创建邮件...")
            msg = MIMEMultipart()
            msg['From'] = "Notify Mate" + "<" + sender_email + ">"
            msg['To'] = receiver_email
            msg['Subject'] = "新加坡汇率通知"
            body = f"当前SGD汇率为{current_rate}，低于设定阈值{threshold_rate}，可以考虑购汇！"
            msg.attach(MIMEText(body, 'plain'))

            # 发送邮件
            print("正在发送邮件...")
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # 启动TLS加密
            server.login(sender_email, password)
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
            server.quit()
            print(f"已发送汇率低于阈值通知邮件至 {receiver_email}")
        
        # 查询间隔
        time.sleep(query_interval)
except KeyboardInterrupt:
    print("程序已停止")
