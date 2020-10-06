import lightbulb
import hikari

class Coronavirus(lightbulb.Plugin):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
    
    @lightbulb.command()
    async def stuff(self, ctx):
        """stuff"""
        pass
    
def load(bot):
    bot.add_plugin(Coronavirus(bot))