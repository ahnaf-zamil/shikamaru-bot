import hikari
from hikari import presences
import lightbulb

class Events(lightbulb.Plugin):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @lightbulb.listener(hikari.ShardReadyEvent)
    async def on_ready(self, event):
        # Event handler for when the bot gets ready
        await self.bot.update_presence(activity=presences.Activity(name="sh!help", type="PLAYING"), status="dnd")
        print("\n\nI'm is ready for work! What a drag.......\n\n")

def load(bot):
    bot.add_plugin(Events(bot))
