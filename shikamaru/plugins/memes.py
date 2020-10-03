import lightbulb
import hikari
import aiohttp
import os
import json
from ..utils.http import fetch, post


class Memes(lightbulb.Plugin):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.imgflipuser = os.environ["IMGFLIPUSER"]
        self.imgflippass = os.environ["IMGFLIPPASS"]

    async def make_meme(self, ctx, text, id):
        msg = await ctx.reply("Please wait....")
        obj = {
            "template_id": str(id),
            "text0": text[:80],
            "text1": "",
            "username": self.imgflipuser,
            "password": self.imgflippass,
        }
        async with aiohttp.ClientSession() as session:
            r = await post(session, url=self.bot.config["meme_api"], data=obj)
            r = json.loads(r)
        await msg.delete()
        await ctx.reply(r["data"]["url"])

    @lightbulb.command()
    async def changemymind(self, ctx, *, text=None):
        """Generates a change my mind meme with given text"""
        if text:
            await self.make_meme(ctx, text, 129242436)
        else:
            await ctx.reply("Please enter text that I can use to create a meme.")

    @lightbulb.cooldown(10, 1, lightbulb.cooldowns.UserBucket)
    @lightbulb.command()
    async def draw25(self, ctx, *, text=None):
        """Generates a draw 25 meme with given text"""
        if text:
            await self.make_meme(ctx, text, 217743513)
        else:
            await ctx.reply("Please enter text that I can use to create a meme.")

    @lightbulb.cooldown(10, 1, lightbulb.cooldowns.UserBucket)
    @lightbulb.command()
    async def monkeypuppet(self, ctx, *, text=None):
        """Generates a monkey puppet meme with given text"""
        if text:
            await self.make_meme(ctx, text, 148909805)
        else:
            await ctx.reply("Please enter text that I can use to create a meme.")


def load(bot):
    bot.add_plugin(Memes(bot))