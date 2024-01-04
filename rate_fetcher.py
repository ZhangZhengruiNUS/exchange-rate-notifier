import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import utils
from decorators import timeit

# 常量定义
BASE_URL = 'https://www.icbc.com.cn/column/1438058341489590354.html'  # 目标URL
MAX_WAIT_TIME = 30  # 最大等待时间，单位秒

@timeit
def get_sgd_rate():
    
    found = False  # 标记是否找到数据
    exchange_rate = 0.0  # 存储汇率值
    driver = None
        
    try:
        # 获取当前脚本的目录
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # 设置ChromeDriver的相对路径（相对于当前脚本）
        chrome_driver_path = os.path.join(current_dir, 'chromedriver')

        # 然后创建Service时使用这个路径
        s = Service(chrome_driver_path)

        # 初始化webdriver
        print("[" + utils.get_current_time() + "] 初始化webdriver...")
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")  # 绕过操作系统安全模型，必须是第一个选项
        chrome_options.add_argument("--disable-dev-shm-usage")  # 解决资源限制的问题

        driver = webdriver.Chrome(service=s, options=chrome_options)

        # 打开目标网页
        print("[" + utils.get_current_time() + "] 正在打开网页...")
        driver.get(BASE_URL)

        # 定位到表格的父元素，确保表格加载完成
        print("[" + utils.get_current_time() + "] 等待网页数据动态加载...")
        wait = WebDriverWait(driver, MAX_WAIT_TIME)  # 最多等待时间
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.el-table--mini')))  # 需要根据实际页面结构确定

        # 定位到外汇信息的表格
        print("[" + utils.get_current_time() + "] 正在定位数据...")
        rows = driver.find_elements(By.XPATH, '//tr[contains(@class, "el-table__row")]')

        # 遍历表格行，寻找新加坡元的现汇卖出价
        
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')
            currency = cells[0].text.strip()  # 币种名称
            if "新加坡元(SGD)" in currency:
                exchange_rate = float(cells[3].text.strip())  # 现汇卖出价
                print("[" + utils.get_current_time() + "] 新加坡元(SGD)的现汇卖出价为: " + str(exchange_rate))
                found = True
                break

        if not found:
            print("[" + utils.get_current_time() + "] 没有找到新加坡元的现汇卖出价")

    except TimeoutException as e:
        print("[" + utils.get_current_time() + "] 页面加载超时: " + str(e))

    finally:
        # 无论成功或失败都尝试关闭浏览器
        if driver is not None:
            driver.quit()
    
    # 返回获取到的汇率
    return found, exchange_rate

if __name__ == "__main__":
    rate = get_sgd_rate()
