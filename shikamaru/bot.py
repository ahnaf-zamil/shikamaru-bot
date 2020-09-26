import lightbulb
import hikari
import logging
from configparser import ConfigParser

# Using configparser to use config.ini file
config_object = ConfigParser()
config_object.read("config.ini")
botconfig = config_object["BOTCONFIG"]

# Setting up logging
logging.getLogger("lightbulb").setLevel(logging.DEBUG)

bot = lightbulb.Bot(token=botconfig['token'], prefix=botconfig['prefix'], insensitive_commands=bool(botconfig['insensitive']), owner_ids=botconfig['owners'])
