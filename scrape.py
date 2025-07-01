from configparser import ConfigParser
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
import requests
import sys
import time

# Read variables from configuation file
config = ConfigParser()
config.read("config.ini")

profile_path = r"{}".format(config.get("FIREFOX", "profile_path"))
# print(profile_path)

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

# --- SCRAPE LISTING PAGE FOR IMPORTANT PRODUCT DETAILS ---
attributes = dict()

# Scroll to "bottom" of the webpage, wait for dynamic content to load
time.sleep(5)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)

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

# Debug Only
print(attributes)

# --- DOWNLOAD LISTING PHOTOS --- 
OUTPUT_FOLDER = "images"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Parse the page with BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")

# Extract image URLs
image_urls = set()

for img in soup.find_all("img"):
    src = img.get("src") or img.get("data-src")
    # Only extract high res images (1600) 
    if src and "s-l1600" in src:
        image_urls.add(src)

# Debug Only
print(image_urls)

for idx, img_url in enumerate(image_urls):
    try:
        response = requests.get(img_url, timeout=10)
        if response.status_code == 200:
            filename = os.path.join(OUTPUT_FOLDER, f"image_{idx + 1}.jpg")
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {filename}")
    except Exception as e:
        print(f"Failed to download {img_url}: {e}")

driver.quit() 


