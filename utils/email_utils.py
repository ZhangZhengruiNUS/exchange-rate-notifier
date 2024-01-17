import os
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from logger_config import setup_logger

logger = setup_logger(__name__)

def send_email(subject, msg_body, config, image_path=None):
    # 创建邮件
    logger.info("正在创建邮件...")
    msg = MIMEMultipart()
    msg['From'] = "Notify Mate" + "<" + config.get_parameter('SENDER_EMAIL') + ">"
    msg['To'] = config.get_parameter('RECEIVER_EMAIL')
    msg['Subject'] = subject

    # 添加图片
    if image_path is not None:
        if os.path.exists(image_path):
            with open(image_path, 'rb') as f:
                img = MIMEImage(f.read())
            img.add_header('Content-ID', '<image1>')  # 注意：在这里，"<image1>"需要是唯一的
            msg.attach(img)

            # 添加HTML正文，其中包含对图片的引用
            html = f"""
            <html>
            <body>
                <p>{msg_body}</p>
                <img src="cid:image1" style="width:90% !important;">
            </body>
            </html>
            """
            msg.attach(MIMEText(html, 'html'))
        else:
            logger.error(f"图片路径无效：{image_path}")
    else:
        msg.attach(MIMEText(msg_body, 'plain'))
    
    # 发送邮件
    logger.info("正在发送邮件...")
    server = smtplib.SMTP(config.get_parameter('SMTP_SERVER'), int(config.get_parameter('SMTP_PORT')))
    server.starttls()  # 启动TLS加密
    server.login(config.get_parameter('SENDER_EMAIL'), config.get_parameter('PASSWORD'))
    text = msg.as_string()
    server.sendmail(config.get_parameter('SENDER_EMAIL'), config.get_parameter('RECEIVER_EMAIL'), text)
    server.quit()
    logger.info(f"已发送邮件至{config.get_parameter('RECEIVER_EMAIL')}")
    
if __name__ == "__main__":
    pass