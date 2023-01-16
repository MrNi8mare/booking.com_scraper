
# ask Sir what else does he need






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
import pandas as pd
from datetime import datetime
import csv
import requests
from selenium.webdriver.common.action_chains import ActionChains








def get_details(driver, url):

    
    start_time = time.time()
        
    driver.get(url)
    
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
            
    html=driver.page_source
    
    soup= BeautifulSoup(html, 'html.parser')
    
    title_div= soup.find('h2', class_='pp-header__title')
    title= title_div.text

    try:
        full_location_div= soup.find('span', class_='jq_tooltip')
        full_location= full_location_div.text
    except:
        print('except 51')
        full_location=None
        
    try:
        location_script= driver.find_element(By.XPATH, '//*[@id="b2hotelPage"]/script[26]')
        location_text= location_script.get_attribute('innerHTML')
    except:
        print('except 58')

        location_text=None
        
    match = re.search(r'(?:latitude|b_map_center_latitude)\s*=\s*(-?\d+\.\d+)', location_text)
    latitude = float(match.group(1)) if match else None

    match = re.search(r'(?:longitude|b_map_center_longitude)\s*=\s*(-?\d+\.\d+)', location_text)
    longitude = float(match.group(1)) if match else None
    
    try:
        rating_div= soup.find('div', class_='d10a6220b4')
        rating= rating_div.text
    except:
        rating=None
        
    try:
        review_div= soup.find('div', class_='db63693c62')
        review_text= review_div.text
    except:
        review_text=None
    
    features_all=''
    try:
        for features in soup.find_all('div', class_='fe87d598e8'):
            features_all=features_all+features.text+','
    except:
        pass
    
    
    reviews=''
    
    for char in review_text:
        
        try:
            char=int(char)
            reviews= reviews+str(char)
        except:
            pass
            
    text_location= html.find("Prices for upcoming dates start at PKR")
    if  text_location!= -1:
        price_text= html[text_location+37:text_location+45]   
        price=''
        for char in price_text:
            try:
                char=int(char) 
                price= price+str(char)
            except:
                pass 
                   
        
    else:
        print("Text not found.")
        
    try:
        driver.execute_script("document.getElementsByClassName('js-bh-photo-grid-item-see-all')[0].click();")
    except:
        pass
    # time.sleep(2)
    
    html=driver.page_source
    soup= BeautifulSoup(html, 'html.parser')
    
    img_string=''

    try:
        img_divs= soup.find_all('div', class_='bh-photo-modal-masonry-grid-item')
        img_count=0
    except:
        pass
    
    for div in img_divs:
        try:
            img_count=img_count+1
            
            a_element=(div.find('a', href=True))
            href = a_element['href']
            img_string=img_string+(' '+href+' ')
        except:
            pass
    
    try:
        with open('Details.csv', 'a', newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow([heading, city, region, title, full_location, rating, reviews, price, longitude, latitude, features_all,  img_string, img_count, url])
    except:
        print('skipped: '+url)

    # print('Time taken: ', time.time() - start_time)
    
    
# options = webdriver.ChromeOptions()

df = pd.read_csv('file.csv')

options = webdriver.FirefoxOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-extensions")

# driver = webdriver.Chrome(options=options)
driver = webdriver.Firefox(options=options)


with open('All_Detail_Links.csv') as f:
    rows = list(csv.reader(f))
    
    for a in range(len(rows)):
    
        row = rows[a]
        
        heading=row[0]
        city= row[1]
        region= row[2]
        url= row[3]
        
        get_details(driver, url)

    driver.quit()
