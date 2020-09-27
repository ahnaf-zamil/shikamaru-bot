import lightbulb
import hikari
import datetime
import psutil
import time
import sqlite3
from ..utils import db
import itertools
import datetime
from platform import python_version


start_time = datetime.datetime.utcnow()

class Info(lightbulb.Plugin):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.process = psutil.Process()

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

    @lightbulb.command()
    async def about(self, ctx):
        """Tells you information about the bot itself."""
        now = datetime.datetime.utcnow()  # Timestamp of when uptime function is run
        delta = now - start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        if days:
            time_format = (
                "**{d}** days, **{h}** hours, **{m}** minutes, and **{s}** seconds."
            )
        else:
            time_format = "**{h}** hours, **{m}** minutes, and **{s}** seconds."
        uptime_stamp = time_format.format(
            d=days, h=hours, m=minutes, s=seconds)
        embed = hikari.Embed()
        embed.title = 'About Shikamaru'
        embed.colour = "#326fa8"
        embed.url = "https://github.com/ahnaf-zamil/shikamaru-bot"

        owner = await self.bot.rest.fetch_user(int(self.bot.owner_ids[0]))
        embed.set_thumbnail(self.bot.me.avatar_url)
        embed.add_field(name="Owner", value=f":point_right: {owner} :point_left:")
        # Statistics
        total_members = 0
        chn = 0
        guilds = 0
        for guild in self.bot.cache.get_available_guilds_view().values():
            guilds += 1
            total_members += guild.member_count
            for channel in guild.channels:
                chn += 1
        t = t = f"""```py
Python Version: {python_version()}
Hikari Version: {hikari.__version__}
SQLite3 Version: {sqlite3.version}
```
        """
        embed.add_field(name='Users', value=f'{total_members}', inline=True)
        embed.add_field(name='Servers', value=f'{len([server async for server in self.bot.rest.fetch_my_guilds()])}', inline=True)
        embed.add_field(name='Channels', value=f'{chn} total', inline=True)
        memory_usage = self.process.memory_full_info().uss / 1024**2
        cpu_usage = self.process.cpu_percent() / psutil.cpu_count()
        embed.add_field(name='Process', value=f'```Memory: {memory_usage:.2f} MiB\nCPU: {cpu_usage:.2f}%```', inline=True)
        version = hikari.__version__
        embed.add_field(name='Commands Ran', value=db.session.query(db.BotData).first().command_ran, inline=True)
        embed.add_field(name='Uptime', value=uptime_stamp)
        embed.add_field(name="Libraries", value=t)
        embed.set_footer(text=f'Made with Hikari v{version}', icon='http://i.imgur.com/5BFecvA.png')
        embed.timestamp = datetime.datetime.now().astimezone()
        await ctx.reply(embed=embed)

    @lightbulb.command()
    async def github(self, ctx):
        em = hikari.Embed(title="Shikamaru's GitHub", color="#4dffa6")
        em.description = "[Click here](https://github.com/ahnaf-zamil/shikamaru-bot) to go to Shikamaru's GitHub page"
        em.set_footer(text=str(self.bot.me), icon=self.bot.me.avatar_url)
        em.timestamp = datetime.datetime.now().astimezone()
        await ctx.reply(embed=em)

def load(bot):
    bot.add_plugin(Info(bot))
