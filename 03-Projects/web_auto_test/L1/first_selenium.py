from selenium import webdriver
driver = webdriver.Chrome()
driver.get("https://ceshiren.com")
print(driver.title)
driver.quit()
