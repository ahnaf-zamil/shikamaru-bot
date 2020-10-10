import sys
import hikari
import lightbulb
import asyncio
import traceback
import aiofiles
from datetime import datetime


class Events(lightbulb.Plugin):
    """The plugin for handling all Hikari events"""

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @lightbulb.listener(hikari.ShardReadyEvent)
    async def on_ready(self, event):
        await self.bot.update_presence(
            activity=hikari.Activity(
                name=f"{self.bot.prefix}help in {len([server async for server in self.bot.rest.fetch_my_guilds()])} servers | What a drag....",
                type=hikari.ActivityType.WATCHING,
            )
        )
        print("""\n\n
   _____ _                                                                                               
  / ____| |   (_) |                                    (_)                        | |      
 | (___ | |__  _| | ____ _ _ __ ___   __ _ _ __ _   _   _ ___   _ __ ___  __ _  __| |_   _ 
  \___ \| '_ \| | |/ / _` | '_ ` _ \ / _` | '__| | | | | / __| | '__/ _ \/ _` |/ _` | | | |
  ____) | | | | |   < (_| | | | | | | (_| | |  | |_| | | \__ \ | | |  __/ (_| | (_| | |_| |
 |_____/|_| |_|_|_|\_\__,_|_| |_| |_|\__,_|_|   \__,_| |_|___/ |_|  \___|\__,_|\__,_|\__, |
                                                                                      __/ |
                                                                                     |___/ 
              \n\n""")

    @lightbulb.listener(hikari.MessageCreateEvent)
    async def on_message(self, event):
        if f"<@!{self.bot.me.id}>" in event.message.content:
            await event.channel.send(
                "What a drag....."
            )  # Sending message when pinged or mentioned.
            return

    @lightbulb.listener(lightbulb.events.CommandErrorEvent)
    async def on_command_error(self, event):
        # Logging error to file and printing it to the standard output
        if (
            type(event.exception) == lightbulb.errors.CommandIsOnCooldown
        ):  # Checking if error is a cooldown error
            # If error is a cooldown error then the bot is sending a cooldown message to the channel.
            channel = await self.bot.rest.fetch_channel(event.message.channel_id)
            em = hikari.Embed(title="Command on cooldown", color="#ff0000")
            em.add_field(
                name="Hold up man!",
                value=f"This command is on cooldown. You can run it in **{int(event.exception.retry_in)}** seconds.",
            )
            em.timestamp = datetime.now().astimezone()
            await channel.send(em)
            return
        now = datetime.now()
        tinfo = traceback.format_exception(
            type(event.exception), event.exception, tb=event.traceback
        )
        print("".join(tinfo))
        error = (
            f"{now.strftime('%Y-%m-%d %H:%M:%S')} [Command Error] User: \"{event.message.author}\", Message: \"{event.message.content[:30]}\", Error: \"{event.exception}\", Traceback: \""
            + "".join(tinfo).replace("\n", "")
            + '"'
        )
        async with aiofiles.open("bot.log", "a+") as f:
            await f.write(f"{error}\n")


def load(bot):
    bot.add_plugin(Events(bot))
