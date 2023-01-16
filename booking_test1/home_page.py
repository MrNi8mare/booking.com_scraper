
# not able to get ayubia and muzaffarabad with headless mode 
# after trying to get the data with headless mode, the script is not working even if srolled using javascript
# after opening the link for each city, we need to go to the see all page which will be the listing page


# ask if they need all the data or just the top listings for each top city



from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import json
import sys
from datetime import datetime
import csv
import requests


def get_listings_from_home_page(driver):
    
    url= 'https://www.booking.com/country/pk.html'
    
    driver.get(url)
    
    html=driver.page_source
    
    with open('booking.html', 'w', encoding='utf-8') as f:
        f.write(html)
        
    soup= BeautifulSoup(html, 'html.parser')
        
    top_div= soup.select('div.bui-carousel.bui-carousel--medium')
    
    for i in range(0,2):
        
        heading= soup.find_all('h2', {'class': 'bui-segment-header'})[i].text

        # print(heading)
    
        top_dest_div= top_div[i]
        top_dest_div_ul=top_dest_div.find('ul')
        
        top_dest_div_li=top_dest_div_ul.find_all('li')
            
        for links in top_dest_div_li:
            
            a_element=(links.find('a', href=True))
            href = a_element['href']
            main_listing_link=('https://www.booking.com'+href)
            
            driver.get(main_listing_link)

            driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")

            
            try:
                driver.find_element(By.XPATH, '//*[@id="c-lp-top-hotels"]/div[2]/div[4]/div[11]/a').click()
            except:
                try:
                    driver.find_element(By.XPATH, '//*[@id="c-lp-top-hotels"]/div[2]/div[4]/div[5]/a').click()
                except:
                    try:
                        driver.find_element(By.XPATH, '//*[@id="c-lp-top-hotels"]/div[2]/div[3]/div[11]/a').click()
                    except:
                        try:
                            driver.find_element(By.XPATH, '//*[@id="c-lp-top-hotels"]/div[2]/div[4]/div[4]/a').click()
                        except:
                            driver.find_element(By.XPATH, '//*[@id="c-lp-top-hotels"]/div[2]/div[3]/div[10]/a').click()
                        
                
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="left_col_wrapper"]/div[1]/div/div/form/div/div[1]/div')))
            
            all_listing_link= driver.current_url
            # print(all_listing_link)
            
            with open('All_Listing_Links.csv', 'a', newline='', encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow([heading, all_listing_link, url])


options = webdriver.ChromeOptions()

# options = webdriver.FirefoxOptions()
# options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-extensions")

driver = webdriver.Chrome(options=options)

get_listings_from_home_page(driver)

driver.quit()
