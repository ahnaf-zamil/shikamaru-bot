import lightbulb
import hikari
import datetime
import psutil
import time
import os
import aiofiles
import sqlite3
import itertools
import datetime
import platform
import asyncio
import googletrans


start_time = datetime.datetime.utcnow()


class Info(lightbulb.Plugin):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.process = psutil.Process(os.getpid())

    @lightbulb.command()
    async def ping(self, ctx):
        """Shows you the bot's latency to the Discord API"""
        start = time.monotonic()
        msg = await ctx.reply("Pinging...")
        millis = (time.monotonic() - start) * 1000
        # Since sharded bots will have more than one latency, this will average them if needed.
        heartbeat = self.bot.heartbeat_latency * 1000
        em = hikari.Embed(title=":ping_pong: Pong! :ping_pong:", color="#00a136")
        em.add_field(name="REST API", value=f"`{int(millis):,.2f}ms`", inline=True)
        em.add_field(
            name="Websocket Gateway", value=f"`{int(heartbeat):,.2f}ms`", inline=True
        )
        em.set_footer(text=str(self.bot.me), icon=self.bot.me.avatar_url)
        em.timestamp = datetime.datetime.now().astimezone()
        await msg.delete()
        await ctx.reply(embed=em)

    @lightbulb.command()
    async def about(self, ctx):
        """Tells you about the bot itself."""
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
        uptime_stamp = time_format.format(d=days, h=hours, m=minutes, s=seconds)
        embed = hikari.Embed(
            title="About Shikamaru",
            color="#326fa8",
            url="https://github.com/ahnaf-zamil/shikamaru-bot",
        )
        owner = await self.bot.rest.fetch_user(int(self.bot.owner_ids[0]))
        embed.set_thumbnail(self.bot.me.avatar_url)
        embed.add_field(name="Owner", value=f":point_right: {owner} :point_left:")
        # Statistics
        t = t = f"""```py
Python Version: {platform.python_version()}
Hikari Version: {hikari.__version__}
```
        """
        osinfo = platform.uname()
        pid = os.getpid()
        py = psutil.Process(pid)
        loop = asyncio.get_running_loop()
        ram_usage = await loop.run_in_executor(None, self.process.memory_full_info)
        ram_usage = ram_usage.rss / 1024**2
        cpu_usage = await loop.run_in_executor(None, self.process.cpu_percent) / await loop.run_in_executor(None, psutil.cpu_count)
        embed.add_field(
            name="OS", value=f"{osinfo.system} {osinfo.version} {osinfo.machine}"
        )
        
        embed.add_field(name="Uptime", value=uptime_stamp)
        embed.add_field(name="Commands loaded", value=len(list(self.bot.commands)))
        embed.add_field(
            name="Process",
            value=f"```Memory: {ram_usage:.2f} MB\nCPU: {psutil.cpu_percent(interval=None, percpu=False)}%```",
            inline=True,
        )
        embed.add_field(name="Libraries", value=t)
        embed.set_footer(text=str(self.bot.me), icon=self.bot.me.avatar_url)
        embed.timestamp = datetime.datetime.now().astimezone()
        await ctx.reply(embed=embed)

    @lightbulb.command()
    async def github(self, ctx):
        """
        Gives link to Shikamaru's GitHub repository
        """
        em = hikari.Embed(title="Shikamaru's GitHub", color="#4dffa6")
        em.description = "[Click here](https://github.com/ahnaf-zamil/shikamaru-bot) to go to Shikamaru's GitHub page"
        em.set_footer(text=str(self.bot.me), icon=self.bot.me.avatar_url)
        em.timestamp = datetime.datetime.now().astimezone()
        em.set_footer(text=str(self.bot.me), icon=self.bot.me.avatar_url)
        await ctx.reply(embed=em)

    @lightbulb.command()
    async def invite(self, ctx):
        """Invite me to your server"""
        await ctx.reply(f"**{ctx.message.author.username}**, use this link to invite me\n<https://discord.com/api/oauth2/authorize?client_id={self.bot.me.id}&permissions={self.bot.config['permissions']}&scope=bot>")

def load(bot):
    bot.add_plugin(Info(bot))
