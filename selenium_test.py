
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
# driver = webdriver.Edge()
# driver.get("https://edition.cnn.com/")
# page_source = driver.page_source
# print(title)
# print(page_source)

def sel_policy(homepage_surl, sfilename):
    driver = webdriver.Edge()
    driver.implicitly_wait(10)
    driver.get(homepage_surl)
    title = driver.title
    print(title)
    sterm_url = None
    elements = driver.find_elements(By.TAG_NAME , "a")
    print("Found!")
    for value in elements:
        if value.text.lower() in ["terms of service", "terms", "terms of use", "steam subscriber agreement", "subscriber agreement", "terms & conditions" , "terms and conditions", "legal", "terms and privacy notice"]:
            print(value.text)
            print(value.get_attribute("href"))
            sterm_url  = value.get_attribute("href")

    if sterm_url is None:
        print("No url found")
        return

    driver.get(sterm_url)
    elements1 = driver.find_element(By.TAG_NAME, "p")
    print(elements1.text)

    page_sourceterm = driver.page_source
    # print(page_sourceterm)

    sourceterms_soup = BeautifulSoup(page_sourceterm, "html.parser")
    pages_text = sourceterms_soup.get_text(separator='\n' , strip=True)
    # print(len(pages_text))

    with open(sfilename, "w", encoding='utf-8') as f:
        f.write(pages_text)

homepage_surl = input("Enter url: ")
sfilename = input("Enter file name:" )
sel_policy(homepage_surl,sfilename)


input()
driver.quit()

