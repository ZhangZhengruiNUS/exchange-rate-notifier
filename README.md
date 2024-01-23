# 汇率通知器
*注意：查询数据爬取自国内某银行官网。部分爬取规则可能随着网站页面更新而失效，仅供参考！*

## 项目描述
汇率通知器是一个旨在实时跟踪并通知用户汇率变化的Python应用程序。当指定的货币对汇率低于预设阈值时，应用程序会自动发送通知邮件给用户。可部署在云服务器中。

## 指南

### 基础准备

1. **确保Python和pip已安装**:
   项目运行需要Python环境，确保你的系统中已经安装了Python和pip。

2. **安装Chrome浏览器**:
   由于项目依赖于Chrome浏览器，确保你的系统中安装了它。Linux用户可以访问 [Chrome下载页面](https://www.google.com/intl/zh-CN/chrome/next-steps.html?platform=linux&statcb=0&installdataindex=empty&defaultbrowser=0#) 获取安装包。

   - 对于Ubuntu系统，下载 `google-chrome-stable_current_amd64.deb` 文件后，使用以下命令安装Chrome浏览器：

     ```bash
     sudo dpkg -i google-chrome-stable_current_amd64.deb
     ```

   - 如果安装时遇到依赖问题，使用以下命令解决：

     ```bash
     sudo apt-get install -f
     ```

   - 通过以下命令检查Chrome浏览器版本，以验证安装是否成功：

     ```bash
     google-chrome --version
     ```

3. **下载Chrome驱动**:
   确保下载的Chrome驱动版本与你的Chrome浏览器版本相兼容。可以在 [Chrome驱动下载页面](https://googlechromelabs.github.io/chrome-for-testing/) 找到最新的驱动。  
   *记住驱动保存的路径/path/to/chromedriver。本项目默认放在项目根目录，如果放在其它地方，之后请自行修改代码里的驱动路径*

   - 下载后，给予驱动执行权限：

     ```bash
     chmod +x /path/to/chromedriver
     ```

   - 可以通过以下命令检查驱动版本：

     ```bash
     /path/to/chromedriver --version
     ```

### 安装项目

1. **克隆仓库**  
*确保你的系统中已经安装了Git*

    ```bash
    git clone https://github.com/yourusername/exchange-rate-notifier.git
    ```

2. **导航到项目目录**
    ```bash
    cd exchange-rate-notifier
    ```

3. **安装依赖**
    ```bash
    pip install -r requirements.txt
    ```

## 使用说明

1. **设置环境变量**  
在项目根目录下创建一个`.env`文件，并定义以下变量：
- `ENV_TYPE`: 环境类型（若设置为"production"，则日志不输出到控制台）
- `SENDER_EMAIL`: 发送通知的邮箱地址
- `RECEIVER_EMAIL`: 接收通知的邮箱地址
- `PASSWORD`: 发送者邮箱账户的密码或应用专用密码
- `SMTP_SERVER`: 发送者邮箱账户的SMTP服务器地址
- `SMTP_PORT`: SMTP服务器端口
- `RATE_THRESHOLD`: 汇率阈值
- `MISSING_DATA_THRESHOLD`: 连续未找到数据的阈值
- `QUERY_INTERVAL`: 检查汇率的时间间隔（以秒为单位）
- `PLOT_PATH`: 绘制图片路径
- `PLOT_RECENT_DAYS`: 绘制图片数据的最近天数
- `LOG_LEVEL`: 日志级别（INFO/DEBUG）
- `NOTIFY_START_TIME`: 每日邮件通知开始时间（格式：MM:SS）
- `NOTIFY_END_TIME`: 每日邮件通知结束时间（格式：MM:SS）

2. **运行应用程序:**
    ```python
    python main.py
    ```