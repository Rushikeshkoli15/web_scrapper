"""
Usage - crawl script for https://www.bigstockphoto.com/ - result store in json file

Author Of Updation- Rushikesh Koli
"""
import csv
import json
import os
import re
import time
from word2number import w2n
from bs4 import BeautifulSoup
# setup for selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from support_extract_age import extract_age

driver_path = "drivers/chromedriver.exe"
headers = {'Accept-Language': 'en-US'}
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument("--start-maximized")
# options.add_argument('--headless')
options.add_argument("webdriver.chrome.driver=" + driver_path)
driver = webdriver.Chrome()
# driver.get(url)

print("---------------------------------------------------")
from selenium.webdriver.common.action_chains import ActionChains

def scroll_down_slowly(driver, speed=8):
    current_scroll_position, new_height= 0, 1
    while current_scroll_position <= new_height:
        current_scroll_position += speed
        driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
        new_height = driver.execute_script("return document.body.scrollHeight")

def pageNavigation(soup, jsonData):
    global actual_profile
    print("In PageNavigation")
    #all_links = soup.find('div', class_='mosaic_wrapper').find_all('div', class_='media')
    all_links = soup.find('div', id='body_galeria').find_all("img")
    print("Length of all links is ", len(all_links))

    # print("Length of all links is ", len(all_links))
    for main_link in all_links:
        info = {
            "id": "NA",
            "name": "NA",
            "gender": "NA",
            "age": "NA",
            "desc": "NA",
            "height": "NA",
            "profile_photo_url": [],
            "additional_photo_urls": [],
            "posted_date": "NA",
            "hair_color": "NA",
            "eye_color": "NA",
            "race/ethnicity": "NA"
        }

        # f"Age_{age}_count"
        print("main link ---- ",main_link)
        #link = main_link.find('img').get('alt')
        #img_tag = soup.find('img')

        alt_string = main_link.get('alt')
        src_url = main_link.get('data-src')
        print("desc", alt_string)
        desc = alt_string
        age = extract_age(desc.lower())
        actual_profile += 1
        try:
            age1 = age
            info['id'] = actual_profile
            info['desc'] = desc
            info['age'] = str(age1)
            for boy in ['boy', 'Boy', 'man', 'male']:
                if re.search(r'\b' + boy + r'\b', desc):
                    info['gender'] = "Male"
            for girl in ['girl', 'Girl', 'woman', 'housewife', 'schoolgirl', 'lady', 'female']:
                if re.search(r'\b' + girl + r'\b', desc):
                    info['gender'] = "Female"

            info['profile_photo_url'] = src_url
            print(info)
            jsonData.append(info)

        except Exception as e:
            print("exception in PageNavigation  -- ", e)

            pass


actual_profile = 0
for search_age in range(6, 19):
    print("AGE : " + str(search_age) + " years")
    url = "https://www.agefotostock.com/age/en/Search.aspx?query=" + str(search_age) + "+year+old+boy&searchfilters=22"
    # url = "https://www.bigstockphoto.com/search/6-year-old-boy/?people_number=1"

    result_json_file = "data_agefoto/Rushikesh_koli_agefotostock_com_boys_" + str(search_age) + "_yrs.json"
    if os.path.exists(result_json_file):
        os.remove(result_json_file)
    jsonData = []

    driver.get(url)
    actual_profile = 0
    page_count = 0
    flag = False
    while (not flag):
        try:
            time.sleep(5)

            print(driver.current_url)
            try:
                element1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler")))
                print("element cookies ",element1)
                element1.click()
                print("cookies accepted")
            except:
                print("cookie frame not found....")
                pass
            scroll_down_slowly(driver)
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "fa-arrow-right")))
            # print("element ===",element)
            html_data = driver.page_source
            # print("html_data =====",html_data)
            soup = BeautifulSoup(html_data, 'html.parser')



            pageNavigation(soup, jsonData)
            element.click()
        except Exception as f:
            print("Exception  ", f)
            flag = True
            html_data = driver.page_source
            soup = BeautifulSoup(html_data, 'html.parser')
            pageNavigation(soup, jsonData)
        finally:
            page_count += 1
            with open(result_json_file, "w") as jsonFile:
                json.dump(jsonData, jsonFile, indent=4)

    print("page_count   ", page_count)

driver.close()