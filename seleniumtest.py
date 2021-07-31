from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

browser = webdriver.Safari()
webpageurls = []

def readFile(fileName):
    fileObj = open(fileName, "r") #opens the file in read mode
    words = fileObj.read().splitlines() #puts the file into an array
    fileObj.close()
    return words
try:
    webpageurls = readFile("test2.txt")

    # print(webpageurls)

    for url in webpageurls:
        browser.get(url)
        # input = browser.find_element_by_id('kw')
        # input.send_keys('Python')
        # input.send_keys(Keys.ENTER)
        # wait = WebDriverWait(browser, 10)
        # wait.until(EC.presence_of_element_located((By.ID, 'content_left')))
        browser.implicitly_wait(5)

        # print(browser.current_url)
        # print(browser.get_cookies())
        pagesource = browser.execute_script("return document.body.innerHTML;")
        # print(pagesource)
        if "reviewcount" in pagesource:
            # print(pagesource.find("reviewcount"))
            colon=pagesource.find(":", pagesource.find("reviewcount"))
            # print(colon)
            count = pagesource[colon+2:pagesource.find("\"", colon+2)]
            print(count)
finally:
    browser.close()