import lightbulb
import hikari
import time
import datetime

class Info(lightbulb.Plugin):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @lightbulb.command()
    async def ping(self, ctx):

        start = time.monotonic()
        msg = await ctx.reply("Pinging...")
        millis = (time.monotonic() - start) * 1000

        # Since sharded bots will have more than one latency, this will average them if needed.
        heartbeat = self.bot.heartbeat_latency * 1000
        em = hikari.Embed(title=":ping_pong: Pong! :ping_pong:", color="#00a136")
        em.add_field(name="REST API", value=f"`{int(millis):,.2f}ms`", inline=True)
        em.add_field(name="Websocket Gateway", value=f"`{int(heartbeat):,.2f}ms`", inline=True)
        em.set_footer(text=str(self.bot.me), icon=self.bot.me.avatar_url)
        em.timestamp = datetime.datetime.now().astimezone()
        await msg.delete()
        await ctx.reply(embed=em)

def load(bot):
    bot.add_plugin(Info(bot))
