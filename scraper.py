import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
if len(sys.argv)<2:
    print("provide url")
    sys.exit()
url=sys.argv[1]
if not url.startswith("http://") and not url.startswith("https://"):
    url = "http://" + url
def provide_url(url):
    browser=webdriver.Chrome()
    browser.get(url)
    print(browser.title)
    print(browser.find_element(By.TAG_NAME, "body").text)
    for link in browser.find_elements(By.TAG_NAME, "a"):
        href = link.get_attribute("href")
        if href:
            print(href)
    browser.quit()
provide_url(url)

