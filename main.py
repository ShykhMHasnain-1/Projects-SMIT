from bs4 import BeautifulSoup
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


# web_url = "https://tidex.co.uk/collections/all-products"
web_url = "https://www.daraz.pk/all-products/"

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get(web_url)
driver.implicitly_wait(8)

# all_links = []
# product_link_path = "//div[@*='product-card']"
product_link_path = "//div[@class='Bm3ON']//a"
all_product = driver.find_elements(By.XPATH,product_link_path)
# print(all_product)

all_product_links = []
for p in all_product:
    p_links =  p.get_attribute("href")
    all_product_links.extend([p_links])
    # print(all_product_links)
with open("Web Scrapping Project\\Links\\All_links.csv","a") as file:
        writer = csv.writer(file,lineterminator='\n')
        writer.writerows(all_product_links)

     

time.sleep(8)
driver.quit()
