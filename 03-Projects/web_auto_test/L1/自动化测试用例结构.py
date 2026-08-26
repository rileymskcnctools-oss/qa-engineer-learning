import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestDemo01():
  def setup_method(self, method):
    # 实例化chromedriver
    self.driver = webdriver.Chrome()
    # 添加全局隐式等待
    self.driver.implicitly_wait(5)

  def teardown_method(self, method):
    # 关闭driver
    self.driver.quit()

  def test_demo01(self):
    # 访问网站
    self.driver.get("https://www.baidu.com/")
    # 设置窗口
    self.driver.set_window_size(1330, 718)
    # 点击输入框
    self.driver.find_element(By.ID, "kw").click()
    # 输入框输入信息
    self.driver.find_element(By.ID, "kw").send_keys("霍格沃兹测试开发")
    # 点击搜索按钮
    self.driver.find_element(By.ID, "su").click()
    # 等待界面加载
    time.sleep(5)
    # 元素定位后获取文本信息
    res = self.driver.find_element(By.XPATH,"//*[@id='1']/h3/a").get_attribute("text")
    # 打印文本信息
    print(res)
    # 添加断言
    assert "霍格沃兹测试开发" in res
    # 查看界面展示
    time.sleep(5)
