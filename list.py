from configparser import ConfigParser
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

# Read variables from configuration file
config = ConfigParser()
config.read("config.ini")

# URL: Grailed create new listing
url = config.get("GRAILED", "new_listing_url")

profile_path = r"{}".format(config.get("FIREFOX", "profile_path"))
print(profile_path)

# Configure Firefox options
options = Options()
options.add_argument("-profile")
options.add_argument(profile_path)

# Create instance of Firefox webdriver
driver = webdriver.Firefox(options=options)