import lightbulb

class Help(lightbulb.Plugin):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @lightbulb.command()
    async def help(self, ctx):
        await ctx.reply("Unfinished help command")
