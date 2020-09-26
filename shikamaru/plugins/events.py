import hikari
import lightbulb

class Events(lightbulb.Plugin):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @lightbulb.listener(hikari.ShardReadyEvent)
    async def on_ready(self, event):
        print("\n\nI'm is ready for work! What a drag.......\n\n")
