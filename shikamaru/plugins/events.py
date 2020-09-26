import hikari
import lightbulb

class Events(lightbulb.Plugin):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @lightbulb.listener(hikari.ShardReadyEvent)
    async def on_ready(self, event):
        print("\n\n I'm ready for work! What a drag.....\n\n")

def load(bot):
    bot.add_plugin(Events(bot))
