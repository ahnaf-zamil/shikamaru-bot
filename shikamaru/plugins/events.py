import hikari
import lightbulb
import asyncio
from ..utils import db
from lightbulb.events import CommandCompletionEvent

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
        
    @lightbulb.listener(CommandCompletionEvent)
    async def on_command_complete(self, event):
        # Incrementing the number of commands ran
        db.increment()


def load(bot):
    bot.add_plugin(Events(bot))
