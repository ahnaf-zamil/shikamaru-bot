import lightbulb
import hikari
import aiohttp
import os
import json
from io import BytesIO
from ..utils.converters import mention_converter
from ..utils.http import fetch, post


class Memes(lightbulb.Plugin):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.imgflipuser = os.environ["IMGFLIPUSER"]
        self.imgflippass = os.environ["IMGFLIPPASS"]

    async def make_meme(self, ctx, text0, text1, id):
        msg = await ctx.reply("Please wait....")
        obj = {
            "template_id": str(id),
            "text0": text0[:80],
            "text1": text1[:80],
            "username": self.imgflipuser,
            "password": self.imgflippass,
        }
        async with aiohttp.ClientSession() as session:
            r = await post(session, url=self.bot.config["meme_api"], data=obj)
            r = json.loads(r)
        await msg.delete()
        await ctx.reply(r["data"]["url"])

    @lightbulb.cooldown(10, 1, lightbulb.cooldowns.UserBucket)
    @lightbulb.command()
    async def changemymind(self, ctx, *, text=None):
        """Generates a change my mind meme with given text"""
        if text:
            await self.make_meme(ctx, text, "", 129242436)
        else:
            await ctx.reply("Please enter text that I can use to create a meme.")

    @lightbulb.cooldown(10, 1, lightbulb.cooldowns.UserBucket)
    @lightbulb.command()
    async def tomcall(self, ctx, *, text=None):
        """Generates a calling Tom meme with given text"""
        if text:
            async with aiohttp.ClientSession() as session:
                data = await fetch(session, f"https://api.alexflipnote.dev/calling?text={text}")
            bio = BytesIO(data)
            bio.seek(0)
            await ctx.reply(attachment=hikari.Bytes(bio, "tomcall.png"))
        else:
            await ctx.reply("Please enter text that I can use to create a meme.")
            
    @lightbulb.cooldown(10, 1, lightbulb.cooldowns.UserBucket)
    @lightbulb.command()
    async def factsmeme(self, ctx, *, text=None):
        """Generates a facts meme with given text"""
        if text:
            async with aiohttp.ClientSession() as session:
                data = await fetch(session, f"https://api.alexflipnote.dev/facts?text={text}")
            bio = BytesIO(data)
            bio.seek(0)
            await ctx.reply(attachment=hikari.Bytes(bio, "facts.png"))
        else:
            await ctx.reply("Please enter text that I can use to create a meme.")
    
    @lightbulb.cooldown(10, 1, lightbulb.cooldowns.UserBucket)
    @lightbulb.command()
    async def floorislava(self, ctx, user=None):
        """Generates a facts meme with given text"""
        if user:
            if user.startswith("<@"):
                user = await self.bot.rest.fetch_user(await mention_converter(user))
            else:
                await ctx.reply("You need to mention the user")
                return
            async with aiohttp.ClientSession() as session:
                data = await fetch(session, f"https://api.alexflipnote.dev/floor?image={user.avatar_url}&text=lava")
            bio = BytesIO(data)
            bio.seek(0)
            await ctx.reply(attachment=hikari.Bytes(bio, "floorislava.png"))
        else:
            async with aiohttp.ClientSession() as session:
                data = await fetch(session, f"https://api.alexflipnote.dev/floor?image={ctx.message.author.avatar_url}&text=lava")
            bio = BytesIO(data)
            bio.seek(0)
            await ctx.reply(attachment=hikari.Bytes(bio, "floorislava.png"))
    
    @lightbulb.cooldown(10, 1, lightbulb.cooldowns.UserBucket)
    @lightbulb.command()
    async def draw25(self, ctx, *, text=None):
        """Generates a draw 25 meme with given text"""
        if text:
            await self.make_meme(ctx, text, "", 217743513)
        else:
            await ctx.reply("Please enter text that I can use to create a meme.")

    @lightbulb.cooldown(10, 1, lightbulb.cooldowns.UserBucket)
    @lightbulb.command()
    async def monkeypuppet(self, ctx, *, text=None):
        """Generates a monkey puppet meme with given text"""
        if text:
            await self.make_meme(ctx, text, "", 148909805)
        else:
            await ctx.reply("Please enter text that I can use to create a meme.")

    @lightbulb.cooldown(10, 1, lightbulb.cooldowns.UserBucket)
    @lightbulb.command()
    async def nutbutton(self, ctx, *, text=None):
        """Generates a nut button meme with given text"""
        if text:
            await self.make_meme(ctx, "Me", text, 119139145)
        else:
            await ctx.reply("Please enter text that I can use to create a meme.")


def load(bot):
    bot.add_plugin(Memes(bot))