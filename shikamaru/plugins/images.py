import hikari
import lightbulb
import aiohttp
import json
import random
from io import BytesIO
from ..utils.http import fetch
from ..utils.converters import mention_converter

dog_titles = [
    "Is this Akamaru?",
    "I think Kiba will like this dog",
    "This dog is from the Inuzuka clan",
    "I don't know who this dog is",
    "What a drag dogs are....",
    "Some random dog I found at Naruto's house",
]

cat_titles = [
    "Cute cat, right?",
    "Cats > Dogs?",
    "Is this even a cat?",
    "uWu",
    "What a drag cats are....",
    "Some random cat I found at Kiba's house..... why does he have a cat?",
]


class Images(lightbulb.Plugin):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
    
    @lightbulb.cooldown(5, 1, lightbulb.cooldowns.UserBucket)
    @lightbulb.command()
    async def supreme(self, ctx, *, text=None):
        """Generate Supreme logo from text"""
        if text:
            async with aiohttp.ClientSession() as session:
                data = await fetch(
                    session, f"https://api.alexflipnote.dev/supreme?text={text[:20]}"
                )
            bio = BytesIO(data)
            bio.seek(0)
            await ctx.reply(attachment=hikari.Bytes(bio, "supreme.png"))
        else:
            await ctx.reply("Please enter text that I can use to create the logo.")
    
    @lightbulb.cooldown(5, 1, lightbulb.cooldowns.UserBucket)
    @lightbulb.command()
    async def achievement(self, ctx, *, text=None):
        """Generate Minecraft achievement from text"""
        if text:
            async with aiohttp.ClientSession() as session:
                data = await fetch(
                    session, f"https://api.alexflipnote.dev/achievement?text={text[:50]}&icon={random.randint(1,45)}"
                )
            bio = BytesIO(data)
            bio.seek(0)
            await ctx.reply(attachment=hikari.Bytes(bio, "achievement.png"))
        else:
            await ctx.reply("Please enter text that I can use to create the image.")
    
    @lightbulb.cooldown(5, 1, lightbulb.cooldowns.UserBucket)
    @lightbulb.command()
    async def challenge(self, ctx, *, text=None):
        """Generate Minecraft challenge from text"""
        if text:
            async with aiohttp.ClientSession() as session:
                data = await fetch(
                    session, f"https://api.alexflipnote.dev/challenge?text={text[:50]}&icon={random.randint(1,45)}"
                )
            bio = BytesIO(data)
            bio.seek(0)
            await ctx.reply(attachment=hikari.Bytes(bio, "challenge.png"))
        else:
            await ctx.reply("Please enter text that I can use to create the image.")
    
    @lightbulb.cooldown(5, 1, lightbulb.cooldowns.UserBucket)
    @lightbulb.command()
    async def colorify(self, ctx, image_url=None):
        """Generates colourified image from raw image"""
        if image_url == None:
            await ctx.reply("Please enter image url")
            return
        if not image_url.startswith("http"):
            await ctx.reply("Invalid image url")
        hexcode = "#fa391b"
        async with aiohttp.ClientSession() as session:
            data = await fetch(
                session, f"https://api.alexflipnote.dev/colourify?image={image_url}&b={hexcode if hexcode.startswith('#') else '#' + hexcode}"
            )
        bio = BytesIO(data)
        bio.seek(0)
        await ctx.reply(attachment=hikari.Bytes(bio, "colorified.png"))
    
    @lightbulb.cooldown(5, 1, lightbulb.cooldowns.UserBucket)
    @lightbulb.command()
    async def pornhub(self, ctx, text1=None, text2="Hub"):
        """Generates a pornhub logo with given text"""
        if text1:
            async with aiohttp.ClientSession() as session:
                data = await fetch(session, f"https://api.alexflipnote.dev/pornhub?text={text1}&text2={text2}")
            bio = BytesIO(data)
            bio.seek(0)
            await ctx.reply(attachment=hikari.Bytes(bio, "phub.png"))
        else:
            await ctx.reply("Please enter text that I can use to create the logo.")
    
    @lightbulb.cooldown(5, 1, lightbulb.cooldowns.UserBucket)
    @lightbulb.command()
    async def salty(self, ctx, *, image_url=None):
        """Generates a salty image from given image"""
        if image_url:
            async with aiohttp.ClientSession() as session:
                data = await fetch(session, f"https://api.alexflipnote.dev/salty?image={image_url}")
            bio = BytesIO(data)
            bio.seek(0)
            await ctx.reply(attachment=hikari.Bytes(bio, "salty.png"))
        else:
            await ctx.reply("Please enter raw image url that I can use to create the image.")
    
    
    @lightbulb.cooldown(5, 1, lightbulb.cooldowns.UserBucket)
    @lightbulb.command()
    async def captcha(self, ctx, *, text=None):
        """Generate Google Captcha image from text"""
        if text:
            async with aiohttp.ClientSession() as session:
                data = await fetch(
                    session, f"https://api.alexflipnote.dev/captcha?text={text[:500]}"
                )
            bio = BytesIO(data)
            bio.seek(0)
            await ctx.reply(attachment=hikari.Bytes(bio, "captcha.png"))
        else:
            await ctx.reply("Please enter text that I can use to create the image.")
    
    @lightbulb.command()
    async def dog(self, ctx):
        """Gives you a random dog."""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://random.dog/woof") as resp:
                if resp.status != 200:
                    return await ctx.reply("No dog found :(")
                filename = await resp.text()
                url = f"https://random.dog/{filename}"
                if filename.endswith((".mp4", ".webm")):
                    await ctx.reply("No dogs found \\:(")
                else:
                    await ctx.reply(
                        embed=hikari.Embed(
                            title=random.choice(dog_titles), color="#dffc03"
                        ).set_image(url)
                    )

    @lightbulb.cooldown(5, 1, lightbulb.cooldowns.UserBucket)
    @lightbulb.command()
    async def bird(self, ctx):
        """Gives you a random bird"""
        async with aiohttp.ClientSession() as session:
            data = await fetch(
                session, f"https://api.alexflipnote.dev/birb"
            )
        data = json.loads(data)
        await ctx.reply(data['file'])
        
    @lightbulb.cooldown(5, 1, lightbulb.cooldowns.UserBucket)
    @lightbulb.command()
    async def sadcat(self, ctx):
        """Gives you a random cat who is sad :smiling_face_with_tear:"""
        async with aiohttp.ClientSession() as session:
            data = await fetch(
                session, f"https://api.alexflipnote.dev/sadcat"
            )
        data = json.loads(data)
        await ctx.reply(data['file'])
    
    @lightbulb.command()
    async def cat(self, ctx):
        """Gives you a random cat."""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.thecatapi.com/v1/images/search"
            ) as resp:
                if resp.status != 200:
                    return await ctx.reply("No cat found :(")
                js = await resp.json()
                await ctx.reply(
                    embed=hikari.Embed(
                        title=random.choice(cat_titles), color="#dffc03"
                    ).set_image(js[0]["url"])
                )
                
def load(bot):
    bot.add_plugin(Images(bot))