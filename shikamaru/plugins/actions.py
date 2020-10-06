import lightbulb
import hikari
import aiofiles
import random
import datetime
import aiohttp
from io import BytesIO
from ..utils.converters import mention_converter
from ..utils.http import fetch


class Actions(lightbulb.Plugin):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @lightbulb.command()
    async def punch(self, ctx, user: lightbulb.member_converter=None):
        """Punches someone."""
        if user != None:
            async with aiofiles.open("shikamaru/txt/punch_gifs.txt", mode="r") as f:
                responses = await f.readlines()
            embed = hikari.Embed(
                title=f"{ctx.message.author} punched {user}!",
                color="#66fc03",
            )

            embed.set_footer(text=f"Requested by: {ctx.message.author}")
            embed.set_image(random.choice(responses))
            embed.timestamp = datetime.datetime.now().astimezone()
            await ctx.reply(embed)

        else:
            await ctx.reply(f"Mention someone to punch, {ctx.message.author.mention}!")

    @lightbulb.command()
    async def run(self, ctx, user: lightbulb.member_converter=None):
        """Go for a jog or run away from someone"""
        async with aiofiles.open("shikamaru/txt/run_gifs.txt", mode="r") as f:
            gif_ls = await f.readlines()
        if user != None:
            embed = hikari.Embed(
                title=f"{ctx.message.author} is running away from {user}!",
                color="#dba951",
            )
        else:
            embed = hikari.Embed(
                title=f"{ctx.message.author} is running!", color="#dba951"
            )
        embed.set_footer(text=f"Requested by: {ctx.message.author}")
        embed.set_image(random.choice(gif_ls))
        embed.timestamp = datetime.datetime.now().astimezone()
        await ctx.reply(embed)

    @lightbulb.cooldown(5, 1, lightbulb.cooldowns.UserBucket)
    @lightbulb.command()
    async def ship(self, ctx, user1: lightbulb.member_converter=None, user2: lightbulb.member_converter=None):
        """Ship two users"""
        if user1 and user2:
            async with aiohttp.ClientSession() as session:
                data = await fetch(
                    session, f"https://api.alexflipnote.dev/ship?user={user1.avatar_url}&user2={user2.avatar_url}"
                )
            bio = BytesIO(data)
            bio.seek(0)
            await ctx.reply(attachment=hikari.Bytes(bio, "ship.png"))
        else:
            await ctx.reply("Please mention two users to ship")

def load(bot):
    bot.add_plugin(Actions(bot))