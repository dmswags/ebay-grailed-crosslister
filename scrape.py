from configparser import ConfigParser

# Read variables from configuation file
config = ConfigParser()
config.read("config.ini")

profile_path = config.get("FIREFOX", "profile_path")
