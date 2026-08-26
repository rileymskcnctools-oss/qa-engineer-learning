import time

from selenium import webdriver
from selenium.webdriver.common.by import By


def web_locate():
    driver = webdriver.Chrome()
    driver.get("https://vip.ceshiren.com/#/ui_study")
    # 1.ID定位，第一个参数传递定位方式，第二个参数传递定位元素
    # web_element=driver.find_element(By.ID,"locate_id")

    # 2.Name定位
    # 如果没有报错，证明元素找到了
    # 如果报错 no such element 代表元素定位可能出错
    # driver.find_element(By.Name,"locate111111") 错误示例
    # driver.find_element(By.Name, "locate")

    # 3.css selector定位
    # driver.find_element(By.CSS_SELECTOR,"#monica-content-root")

    # 4.XPATH定位
    # driver.find_element(By.XPATH,"/html/body/script[2]")
    # time.sleep(3)


    # 5.通过链接文本的方式定位 1 元素一定是a标签 2 输入的元素为标签内的文本
    # driver.find_element(By.LINK_TEXT,"元素定位")

    # print(web_element)



if __name__ == "__main__":
    web_locate()