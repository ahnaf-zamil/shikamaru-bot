import sys
import hikari
import lightbulb
import asyncio
import traceback
import aiofiles
from ..utils import db
from datetime import datetime

class Events(lightbulb.Plugin):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @lightbulb.listener(hikari.ShardReadyEvent)
    async def on_ready(self, event):
        await self.bot.update_presence(activity=hikari.Activity(
            name=f"sh!help in {len([server async for server in self.bot.rest.fetch_my_guilds()])} servers | What a drag....",
            type=hikari.ActivityType.WATCHING
        ))
        print("\n\n I'm ready for work! What a drag.....\n\n")

    @lightbulb.listener(hikari.MessageCreateEvent)
    async def on_message(self, event):
        if "<@!759338827432722472>" in event.message.content:
            await event.channel.send("What a drag.....") # Sending message when pinged or mentioned.
            return

    @lightbulb.listener(lightbulb.events.CommandCompletionEvent)
    async def on_command_complete(self, event):
        # Incrementing the number of commands ran
        db.increment()

    @lightbulb.listener(lightbulb.events.CommandErrorEvent)
    async def on_command_error(self, event):
        # Logging error to file and printing it to the standard output
        now = datetime.now()
        tinfo = traceback.format_exception(type(event.exception), event.exception,  tb=event.traceback)
        print(''.join(tinfo))
        error = f"{now.strftime('%Y-%m-%d %H:%M:%S')} [Command Error] User: '{event.message.author}', Message: '{event.message.content[:30]}', Error: '{event.exception}', Traceback: " + ''.join(tinfo).replace('\n', ' ')
        async with aiofiles.open("bot.log", "a+") as f:
            await f.write(f"{error}\n")

def load(bot):
    bot.add_plugin(Events(bot))
