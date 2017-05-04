import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

if __name__ == '__main__':
    driver = webdriver.Chrome("../../chromedriver")
    # base_url = "http://ieeexplore.ieee.org/"
    driver.get("http://ieeexplore.ieee.org/search/searchresult.jsp?queryText=Information%20Retrieval&ranges=2000_2017_Year&pageNumber=1&rowsPerPage=100")
    flag = True
    page = 1
    while flag:
        print "page: ", page
        time.sleep(5)
        driver.find_element_by_css_selector("input[type=\"checkbox\"]").click()
        time.sleep(5)
        driver.find_element_by_link_text("Export").click()
        time.sleep(5)
        driver.find_element_by_xpath("(//button[@type='button'])[3]").click()
        time.sleep(5)
        
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        try:
            driver.find_element_by_link_text(">").click()
            page += 1
            time.sleep(5)
        except:
            print "=================="
            print "At the end."
            print page
            print "=================="

        
    
    