from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

browser = webdriver.Safari()
try:
    browser.get('https://www.academy.com/shop/pdp/all-star-classic-series-casting-rod#repChildCatid=4138067')
    # input = browser.find_element_by_id('kw')
    # input.send_keys('Python')
    # input.send_keys(Keys.ENTER)
    # wait = WebDriverWait(browser, 10)
    # wait.until(EC.presence_of_element_located((By.ID, 'content_left')))
    browser.implicitly_wait(5)

    print(browser.current_url)
    print(browser.get_cookies())
    pagesource = browser.execute_script("return document.body.innerHTML;")
    print(pagesource)
finally:
    browser.close()