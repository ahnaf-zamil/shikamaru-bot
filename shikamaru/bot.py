import lightbulb
import hikari
import logging
import asyncio
import os
from configparser import ConfigParser

# Prefix is stored as an environment variable

# Using configparser to use config.ini file
config_object = ConfigParser()
config_object.read("config.ini")
botconfig = config_object["BOTCONFIG"]

# Setting up logging
logging.getLogger("lightbulb").setLevel(logging.DEBUG)

# Instantiating bot
bot = lightbulb.Bot(
    token=os.environ["TOKEN"],
    prefix=botconfig["prefix"],
    insensitive_commands=bool(botconfig["insensitive"]),
    owner_ids=[int(i) for i in botconfig["owners"].split(", ")],
)
bot.prefix = botconfig["prefix"]
bot.config = botconfig
