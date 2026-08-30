from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class TestLocate:
    def setup_method(self):
        self.driver=webdriver.Chrome()
        self.driver.get("https://vip.ceshiren.com/#/ui_study/locate")
        self.driver.maximize_window()

    def teardown_method(self):
        self.driver.quit()

    def test_id(self):
        element=self.driver.find_element(
            By.ID,"located_id"
        )
        element.click()

    def test_class_name(self):
        element = self.driver.find_element(
            By.CLASS_NAME,
            "locate_class_name"
        )

        element.click()

    def test_name(self):
        element = self.driver.find_element(
            By.NAME,
            "located_name"
        )

        element.click()

    def test_link_text(self):
        element = self.driver.find_element(
            By.LINK_TEXT,
            "link"
        )

        element.click()

    def test_partial_link_text(self):
        element = self.driver.find_element(
            By.PARTIAL_LINK_TEXT,
            "partial_link"
        )

        element.click()

    def test_tag_name(self):
        element = self.driver.find_element(
            By.TAG_NAME,
            "tag"
        )

        element.click()

    def test_css_absolute(self):
        element = self.driver.find_element(
            By.CSS_SELECTOR,
            "#app > div > section > section > main > div > div.box2 > div.grandfather > div.pos.father > span > button"
        )

        element.click()

    def test_xpath_absolute(self):
        element = self.driver.find_element(
            By.XPATH,
            "//*[@id='app']/div/section/section/main/div/div[2]/div[2]/div[2]/div/button"
        )

        element.click()

