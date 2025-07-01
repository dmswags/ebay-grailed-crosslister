from configparser import ConfigParser
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import sys

# Read variables from configuation file
config = ConfigParser()
config.read("config.ini")

profile_path = r"{}".format(config.get("FIREFOX", "profile_path"))
print(profile_path)

# Configure Firefox options -- MUST 
options = Options()
options.add_argument("-profile")
options.add_argument(profile_path)


# Create instance of Firefox webdriver
driver = webdriver.Firefox(options=options)