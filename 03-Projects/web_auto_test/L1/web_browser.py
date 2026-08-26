# 导入Selenium的webdriver模块
import time

from selenium import webdriver

def window_start():
    # 创建Chrome浏览器的选项对象
    options = webdriver.ChromeOptions()
    # 初始化Chrome浏览器驱动
    driver = webdriver.Chrome(options=options)
    # 打开网页
    driver.get('https://www.ceshiren.com')
    time.sleep(5)
    # 刷新浏览器
    driver.refresh()
    driver.get('https://www.baidu.com')
    # 退回浏览器
    driver.back()
    # 窗口最大化
    driver.maximize_window()
    time.sleep(3)
    driver.minimize_window()
    time.sleep(3)
    # 关闭浏览器
    driver.quit()

if __name__ == '__main__':
    window_start()
