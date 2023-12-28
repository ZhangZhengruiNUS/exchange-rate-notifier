from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib
from dotenv import load_dotenv

def load_config():
    # 加载基础参数
    load_dotenv()
    config = {
        "sender_email": os.getenv("SENDER_EMAIL"),  # 邮件发送者
        "receiver_email": os.getenv("RECEIVER_EMAIL"),  # 邮件接收者
        "password": os.getenv("PASSWORD"),  # 邮箱密码或专用密码
        "smtp_server": os.getenv("SMTP_SERVER"),  # SMTP服务器地址
        "smtp_port": int(os.getenv("SMTP_PORT")),  # SMTP服务器端口（SSL为465，TLS为587）
        "rate_threshold": float(os.getenv("RATE_THRESHOLD")),  # 汇率阈值（低于此值时发送邮件）
        "missing_data_threshold": int(os.getenv("MISSING_DATA_THRESHOLD")),  # 连续未找到数据的阈值（高于此值时发送邮件）
        "query_interval": int(os.getenv("QUERY_INTERVAL")),  # 查询间隔，单位为秒
    }
    return config

def send_email(subject, msg_body, config):
    # 创建邮件
    msg = MIMEMultipart()
    msg['From'] = "Notify Mate" + "<" + config["sender_email"] + ">"
    msg['To'] = config["receiver_email"]
    msg['Subject'] = subject
    msg.attach(MIMEText(msg_body, 'plain'))

    # 发送邮件
    print("[" + get_current_time() + "] 正在发送邮件...")
    server = smtplib.SMTP(config["smtp_server"], config["smtp_port"])
    server.starttls()  # 启动TLS加密
    server.login(config["sender_email"], config["password"])
    text = msg.as_string()
    server.sendmail(config["sender_email"], config["receiver_email"], text)
    server.quit()
    print("[" + get_current_time() + "] 已发送邮件至 " + config['receiver_email'])

def get_current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')