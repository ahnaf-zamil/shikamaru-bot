import lightbulb
import hikari
import logging
from configparser import ConfigParser

config_object = ConfigParser()
config_object.read("config.ini")
botconfig = config_object["BOTCONFIG"]

logging.getLogger("lightbulb").setLevel(logging.DEBUG)

bot = lightbulb.Bot(token=botconfig['token'], prefix=botconfig['prefix'], insensitive_commands=bool(botconfig['insensitive']), owner_ids=botconfig['owners'])

@bot.command()
async def ping(ctx):
    await ctx.reply("Pong!")
