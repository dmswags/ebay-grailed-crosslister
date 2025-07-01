from configparser import ConfigParser
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

import sys
import time

# Read variables from configuation file
config = ConfigParser()
config.read("config.ini")

profile_path = r"{}".format(config.get("FIREFOX", "profile_path"))
print(profile_path)

# Configure Firefox options
options = Options()
options.add_argument("-profile")
options.add_argument(profile_path)

# Create instance of Firefox webdriver
driver = webdriver.Firefox(options=options)

# Read URL from system arguemnts
url = sys.argv[1]
print(url)

# Navigate to listing page
driver.get(url)

# SCRAPE LISTING PAGE FOR IMPORTANT PRODUCT DETAILS
attributes = dict()

# Scroll to "bottom" of the webpage
time.sleep(2)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)

# Attribute: Title
title_element = driver.find_element(By.CLASS_NAME, "x-item-title__mainTitle")
attributes["title"] = title_element.text

# Attribute: Condition
condition_element = driver.find_element(By.CLASS_NAME, "x-item-condition-text")
temp = (condition_element.text).splitlines()
temp = temp[0]
attributes["condition"] = temp

# Attribute: Price
element = driver.find_element(By.CLASS_NAME, "x-price-primary")

# Remove non-numeric characters with partial string ("US $")
attributes["price"] = (element.text)[4:]

print(attributes)

driver.close()
 
# Unable to Scrape Item Description (iFrame) + Item Specifics (Color, Country of Origin)