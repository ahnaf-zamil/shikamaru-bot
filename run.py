import os
import inspect
import importlib
import shikamaru
from shikamaru import bot

print(f"\n\n\nShikamaru v{shikamaru.__version__} by", shikamaru.__author__, "\n\n\n")

# Loading plugins
# If you are familiar with Discord.py, plugins are similar to cogs
for i in os.listdir('./shikamaru/plugins'):
    if i.endswith(".py"):
        plugin = importlib.import_module(f"shikamaru.plugins.{i[:-3]}")
        plugin.load(bot)

# Running bot
bot.run()
