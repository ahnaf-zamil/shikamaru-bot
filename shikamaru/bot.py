import lightbulb
import hikari
import logging
import os
import importlib
import inspect
from configparser import ConfigParser

config_object = ConfigParser()
config_object.read("config.ini")
botconfig = config_object["BOTCONFIG"]

logging.getLogger("lightbulb").setLevel(logging.DEBUG)

bot = lightbulb.Bot(token=botconfig['token'], prefix=botconfig['prefix'], insensitive_commands=bool(botconfig['insensitive']), owner_ids=botconfig['owners'])
bot.remove_command("help")

@bot.command()
async def ping(ctx):
    await ctx.reply("Pong!")


for i in os.listdir('./shikamaru/plugins'):
    if i.endswith(".py"):
        plugin = importlib.import_module(f"shikamaru.plugins.{i[:-3]}")
        for name, obj in inspect.getmembers(plugin):
            if inspect.isclass(obj):
                bot.add_plugin(obj(bot))
