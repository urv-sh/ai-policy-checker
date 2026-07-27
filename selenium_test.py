
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
driver = webdriver.Edge()
driver.get("https://edition.cnn.com/")
title = driver.title
# page_source = driver.page_source
# print(title)
# print(page_source)
try:
    elements = driver.find_elements(By.PARTIAL_LINK_TEXT , "Terms")
    print("Found!")
    for value in elements:
        print(value.text)
    
    # target.click()
except NoSuchElementException:
    print("not found")


input()

driver.quit()

