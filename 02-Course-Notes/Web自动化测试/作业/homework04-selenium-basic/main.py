"""
需求
1.打开测试人论坛：https://ceshiren.com
2.点击搜索按钮。
3.输入关键字：ChromeDriver。
4.点击高级搜索按钮。
5.断言出现的第一个标题的内容。
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestCeshiren:
    def setup_method(self):
        # 创建浏览器
        self.driver = webdriver.Chrome()

        # 打开练习页面
        self.driver.get(
            "https://ceshiren.com"
        )

        # 最大化窗口
        self.driver.maximize_window()

    def teardown_method(self):
        # 关闭浏览器
        self.driver.quit()

    def test_ceshiren(self):
        #定位搜索按钮点击
        self.driver.find_element(By.ID,"search-button").click()
        # 定位搜索框并输入关键词
        self.driver.find_element(By.ID,"search-term").send_keys("ChromeDriver")
        # 定位高级搜索框，点击高级搜索框
        self.driver.find_element(By.CSS_SELECTOR,"[title='打开高级搜索']").click()

        # 显式等待页面中所有标题出现
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "topic-title")
            )
        )
        # 获取页面所有标题
        titles = self.driver.find_elements(
            By.CLASS_NAME,
            "topic-title"
        )
        # 获取页面第一个标题
        first_title = titles[0].text
        assert "chromedriver" in first_title.lower()



