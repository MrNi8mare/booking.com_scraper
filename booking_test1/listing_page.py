





from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
import json
import re
import sys
from datetime import datetime
import csv
import requests
from selenium.webdriver.common.action_chains import ActionChains




def get_detail_links_from_listing_page(driver, url):
    
    
    driver.get(url)
    break_in_next= False
    
    for i in range(0, 999):
        
            
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
        
        html=driver.page_source
        soup= BeautifulSoup(html, 'html.parser')

        soup.find_all('div', class_='c90a25d457')
        
        city= driver.find_element(By.XPATH, '//*[@id="bodyconstraint-inner"]/div[1]/div/div/div/nav/ol/li[4]/span/a/span')
        city= city.text
        
        
        if city=='Search results':
            city= driver.find_element(By.XPATH, '//*[@id="bodyconstraint-inner"]/div[1]/div/div/div/nav/ol/li[3]/span/a')
            city= city.text
            
        region= driver.find_element(By.XPATH, '//*[@id="bodyconstraint-inner"]/div[1]/div/div/div/nav/ol/li[3]/span/a')
        region= region.text
        
        if break_in_next== True:
            break
        
        break_in_next= False
        length= len(soup.find_all('div', class_='c90a25d457'))
        if length<25:
            break_in_next= True

        for div in soup.find_all('div', class_='c90a25d457'):
            hotel_link= (div.a['href'])
            
            with open('All_Detail_Links.csv', 'a', newline='', encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow([heading, city, region, hotel_link, url])
        
        try:
            driver.execute_script("document.getElementsByClassName('f9d6150b8e')[1].click();")
            time.sleep(1)

        except:
            print('except 66')
            break

options = webdriver.ChromeOptions()

# options = webdriver.FirefoxOptions()
# options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-extensions")

driver = webdriver.Chrome(options=options)

with open('All_Listing_Links.csv') as f:
    rows = list(csv.reader(f))

    for a in range(len(rows)):
    
        row = rows[a]
        
        heading=row[0]
        url= row[1]

        get_detail_links_from_listing_page(driver, url)

    driver.quit()



