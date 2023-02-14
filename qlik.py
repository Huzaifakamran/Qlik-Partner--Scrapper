from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from selenium import webdriver
import time
import configparser
import pandas as pd


def configureWebDriver():
    driver = webdriver.Chrome('C:\chromedriver_win32\chromedriver.exe')
    return driver

driver = configureWebDriver()
driver.get('https://www.qlik.com/us/partners/find-a-partner')
time.sleep(3)
driver.maximize_window()
time.sleep(3)

datalist=[]
select = Select(driver.find_element(By.ID,'zl_countryCode'))
for opt in select.options[1:]:
    print(opt.text)
    select.select_by_visible_text(opt.text)
    time.sleep(3)
    try:
        elements = soup.find('div',class_='zl_partner-tiles')
        print('under try')
    except NoSuchElementException:
        pass

    while True:
        print('under true')
        try:
            button = driver.find_element(By.ID, "zl_show-more-btn")
            print("True")
            driver.execute_script("arguments[0].scrollIntoView();", button)
            driver.execute_script("arguments[0].click();", button)
            time.sleep(3)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "zl_show-more-btn")))
            div = driver.find_element(By.ID, "zl_show-more")
            if div.value_of_css_property("display") == "none":
                print("No more Load More buttons found, exiting the loop.")
                break
        except NoSuchElementException:
            print("No Load More button found")
            break
    soup = BeautifulSoup(driver.page_source,'html.parser')
    elements = soup.find('div',class_='zl_partner-tiles')
  
    data = elements.find_all('div',class_='zl_partner-tile zl_partner-tile-hover')
    for i in range(0,len(data)):
        partner_name = data[i].find('div',class_="zl_partner-name zl_partner-name-hover").text
        
        category = data[i].find('div',class_="zl_partner-tier").text
      
        partner_address = data[i].find('div',class_="zl_partner-address").get_text(separator=" ").strip()
        tier = data[i].find('li',class_="zl_more-details-custom-field")
        if tier != None:
            partner_tier = tier.find('span',class_='zl_value')
            if partner_tier != None:
                partner_tier= partner_tier.text
            else:
                partner_tier = ''
        else:
            partner_tier = ''

        image = data[i].find('div',class_='zl_partner-logo zl_partner-logo-hover')
        img = image.find('img')
        website = data[i].find('div',class_='zl_partner-website')
        if website != None:
            website_url = website.find('a')
            website_url_href = website_url['href']
        else:
            website_url_href=''
        data_dict = {
            'Country': opt.text,
            'PartnerName':partner_name,
            'Category':category,
            'PartnerTier':partner_tier,
            'PartnerAddress':partner_address,
            'ImageURL': img['src'],
            'Website':website_url_href
        }
        datalist.append(data_dict)
df = pd.DataFrame(datalist)
df.to_csv(r'E:\TMC\Qlik Data Scrapper\QlikDataScrapper.csv', index = False, header=True)