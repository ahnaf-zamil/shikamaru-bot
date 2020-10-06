import lightbulb
import hikari
import random
import aiohttp
import json
import asyncio
import datetime
import aiofiles
import googletrans
from io import BytesIO
import urllib.parse
from ..utils.http import fetch
from ..utils.converters import mention_converter


class Fun(lightbulb.Plugin):
    """The plugin for all fun commands"""

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.trans = googletrans.Translator()

    async def qrickit(self, ctx, data):
        em = hikari.Embed(color="#0071d4")
        em.set_author(name=str(ctx.message.author), icon=ctx.message.author.avatar_url)
        em.set_image(f"https://qrickit.com/api/qr.php?d={data}&qrsize=300&t=p&e=m")
        em.set_footer(
            text=f"Requested by: {ctx.message.author}",
            icon=ctx.message.author.avatar_url,
        )
        em.timestamp = datetime.datetime.now().astimezone()
        await ctx.reply(embed=em)

    async def get_meme(self):
        async with aiohttp.ClientSession() as session:
            sub_reddit = self.bot.config["meme_subreddit"].replace(
                "https://reddit.com/r/", ""
            )
            r = await fetch(
                session, "https://meme-api.herokuapp.com/gimme/" + sub_reddit
            )
            r = json.loads(r)

        return r

    async def get_joke(self):
        async with aiohttp.ClientSession() as session:
            r = await fetch(
                session, "https://official-joke-api.appspot.com/jokes/random"
            )
            r = json.loads(r)
        return r

    @lightbulb.command()
    async def meme(self, ctx):
        """Gives you a random meme from Reddit."""
        json_data = await self.get_meme()
        em = hikari.Embed(title=json_data["title"], color="#7bf542")
        em.url = json_data["postLink"]
        em.set_author(
            name=f"By {json_data['author']}",
            url="https://www.reddit.com/user/" + json_data["author"],
        )
        em.set_image(json_data["url"])
        em.set_footer(
            text=f"Requested by: {ctx.message.author}",
            icon=ctx.message.author.avatar_url,
        )
        em.timestamp = datetime.datetime.now().astimezone()
        await ctx.reply(embed=em)

    @lightbulb.cooldown(5, 1, lightbulb.cooldowns.UserBucket)
    @lightbulb.command()
    async def fml(self, ctx):
        """Gives you a f**k my life joke (This command is NSFW)"""
        channel = await self.bot.rest.fetch_channel(ctx.message.channel_id)
        if not channel.is_nsfw:
            await ctx.reply("This command can only be used in NSFW channels.")
            return
        async with aiohttp.ClientSession() as session:
            data = await fetch(session, "https://api.alexflipnote.dev/fml")
            data = json.loads(data)
        em = hikari.Embed(
            title="F**k my file",
            color="#3bff3b",
            description=f"{data['text']}"
        )
        
        em.set_footer(
            text=f"Requested by: {ctx.message.author}",
            icon=ctx.message.author.avatar_url,
        )
        em.timestamp = datetime.datetime.now().astimezone()
        await ctx.reply(em)

    @lightbulb.command()
    async def math(self, ctx, *, expr=None):
        """Does math for you, only the simple ones not algebra or geometry"""
        if expr:
            loop = asyncio.get_running_loop()
            ret = await loop.run_in_executor(None, urllib.parse.quote, expr)
            async with aiohttp.ClientSession() as session:
                result = await fetch(session, f"http://api.mathjs.org/v4/?expr={ret}")
                result = result.decode("utf-8")
            em = hikari.Embed(title="Math", color="#8bfce0")
            em.add_field(name="Expression", value=expr)
            em.add_field(name="Result", value=result)
            em.set_thumbnail("https://i.ibb.co/tb82t15/calculator-icon-math-icon-11563227565ddgk3sskht-1.png")
            em.set_footer(text=str(self.bot.me), icon=self.bot.me.avatar_url)
            em.timestamp = datetime.datetime.now().astimezone()
            await ctx.reply(em)
        else:
            await ctx.reply("Please enter a math expression at the end of the function")
    
    
    @lightbulb.cooldown(5, 1, lightbulb.cooldowns.UserBucket)
    @lightbulb.command()
    async def urban(self, ctx, *, word=None):
        """Search something on the urban dictionary"""
        channel = self.bot.cache.get_guild_channel(ctx.message.channel_id)
        await self.bot.rest.trigger_typing(channel)
        try:
            async with aiohttp.ClientSession() as session:
                data = await fetch(
                    session, f"https://api.urbandictionary.com/v0/define?term={word}"
                )
                data = json.loads(data)
        except Exception:
            return await ctx.reply(
                "Urban API is not working at the moment.... it may be down \:("
            )

        if not data:
            return await ctx.reply("I think the API broke...")

        if not len(data["list"]):
            return await ctx.reply("Couldn't find your search in the dictionary...")

        result = data["list"][0]
        definition = result["definition"]
        if len(definition) >= 1000:
            definition = definition[:1000]
            definition = definition.rsplit(" ", 1)[0]
            definition += "..."

        em = hikari.Embed(
            title=f"Urban definition for {result['word']}", color="#008563"
        )
        em.url = result["permalink"]
        em.add_field(name="Definition", value=result["definition"])
        em.add_field(name="Example", value=result["example"])
        em.add_field(
            name="Info",
            value=f"**Author:** {result['author']}\n**Written on:** {result['written_on']}",
        )
        em.add_field(name="Upvotes :thumbsup:", value=result["thumbs_up"], inline=True)
        em.add_field(
            name="Downvotes :thumbsdown:", value=result["thumbs_down"], inline=True
        )
        em.set_author(name=str(ctx.message.author), icon=ctx.message.author.avatar_url)
        em.set_footer(text=str(self.bot.me), icon=self.bot.me.avatar_url)
        em.timestamp = datetime.datetime.now().astimezone()
        try:
            await ctx.reply(em)
        except:
            await ctx.reply(f"Definition not found for term: {word}")

    @lightbulb.command()
    async def joke(self, ctx):
        """Gives you a random joke off the internet."""
        json_data = await self.get_joke()
        em = hikari.Embed(
            title="Joke",
            color="#d96200",
            description=f"{json_data['setup']}\n" + f"||{json_data['punchline']}||",
        )
        em.set_footer(
            text=f"Requested by: {ctx.message.author}",
            icon=ctx.message.author.avatar_url,
        )
        em.timestamp = datetime.datetime.now().astimezone()
        await ctx.reply(embed=em)

    @lightbulb.cooldown(10, 1, lightbulb.cooldowns.UserBucket)
    @lightbulb.command()
    async def qrcode(self, ctx, *, url: str = None):
        """Creates QRCode out of url"""
        if url:
            await self.qrickit(ctx, url)
            return
        await ctx.reply("Please enter a url to make QRCode")


    @lightbulb.command(name="8ball", aliases=["8ball"])
    async def fortune(self, ctx, *, question: str = None):
        """Test your luck with 8ball."""
        if question:
            async with aiofiles.open("shikamaru/txt/8ball.txt", mode="r") as f:
                responses = await f.readlines()
            await ctx.reply(f"{ctx.message.author.mention}, {random.choice(responses)}")
            return
        await ctx.reply("Ask a question to 8ball.")

    @lightbulb.command()
    async def roast(self, ctx, *, user=None):
        if user:
            with open("shikamaru/txt/roasts.txt") as f:
                roasts = f.readlines()

            await ctx.reply(f"**{user}**, {random.choice(roasts)}")
        else:
            await ctx.reply(
                f"Mention the person you want to roast, {ctx.message.author.mention}"
            )

    @lightbulb.cooldown(5, 1, lightbulb.cooldowns.UserBucket)
    @lightbulb.command()
    async def translate(self, ctx, *, text: str = None):
        """Translate text into many different languages"""
        if text:
            loop = asyncio.get_running_loop()
            try:
                ret = await loop.run_in_executor(None, self.trans.translate, text)
            except Exception as e:
                return await ctx.reply(
                    f"An error occurred: {e.__class__.__name__}: {e}"
                )

            embed = hikari.Embed(title="Translated", colour="#ff002b").set_footer(
                text=f"Requested by: {ctx.message.author}",
                icon=ctx.message.author.avatar_url,
            )
            src = googletrans.LANGUAGES.get(ret.src, "(auto-detected)").title()
            dest = googletrans.LANGUAGES.get(ret.dest, "Unknown").title()
            embed.add_field(name=f"From {src}", value=ret.origin, inline=False)
            embed.add_field(name=f"To {dest}", value=ret.text, inline=False)
            embed.timestamp = datetime.datetime.now().astimezone()
            await ctx.reply(embed=embed)
        else:
            await ctx.reply("Give me text to translate.")

    @lightbulb.command()
    async def f(self, ctx, *, reason=None):
        """Press F to pay respect"""
        hearts = ["❤", "💛", "💚", "💙", "💜"]
        text = f"to **{reason}** " if reason else ""
        await ctx.reply(
            f"**{ctx.author}** has paid their respect {text}{random.choice(hearts)}"
        )
        

    @lightbulb.cooldown(5, 1, lightbulb.cooldowns.UserBucket)
    @lightbulb.command()
    async def hack(self, ctx, *, user):
        """Hack someone's account! Try it!"""
        if user != None:
            username = user.lower()
            if user.startswith("<@"):
                user = await self.bot.rest.fetch_user(await mention_converter(user))
                username = user.username.lower()
            await ctx.reply(f"Initiated HTML script for hacking: {user}!")
            await asyncio.sleep(1)
            msg = await ctx.reply("Connecting to Discord HQ servers....")
            await asyncio.sleep(1)
            await msg.edit(content="Successfully connected to Discord servers!")
            await asyncio.sleep(2)
            msg = await ctx.reply("Injecting CSS code into database...")
            await asyncio.sleep(1)
            await msg.edit(content="Injecting CSS code into database... Success!")
            await asyncio.sleep(2)
            msg = await ctx.reply(
                content="Accessing Discord Database... [:blue_square::blue_square:    ] 15%"
            )
            await asyncio.sleep(2)
            await msg.edit(
                content="Accessing Discord Database... [:blue_square::blue_square::blue_square:   ] 42%"
            )
            await asyncio.sleep(2)
            await msg.edit(
                content="Accessing Discord Database... [:blue_square::blue_square::blue_square::blue_square::blue_square: ] 69%"
            )
            await asyncio.sleep(2)
            await msg.edit(
                content="Accessing Discord Database.... **COMPLETE!** [:blue_square::blue_square::blue_square::blue_square::blue_square::blue_square:] 99.99%"
            )
            await asyncio.sleep(2)

            msg = await ctx.reply("Retrieving Login Info... [:blue_square:      ] 1%")
            await asyncio.sleep(3)
            await msg.edit(
                content="Retrieving Login Info... [:blue_square::blue_square::blue_square:   ] 42%"
            )
            await asyncio.sleep(3)
            await msg.edit(
                content="Retrieving Login Info... [:blue_square::blue_square::blue_square::blue_square::blue_square::blue_square: ] 69%"
            )
            await asyncio.sleep(4)
            if random.choice(["success", "failure", "success"]) == "failure":
                await ctx.reply(
                    f"An error has occurred hacking {user}'s account. Please try again later. ❌"
                )
            else:
                await msg.edit(
                    content="Retrieving Login Info.... **COMPLETE!** [:blue_square::blue_square::blue_square::blue_square::blue_square::blue_square::blue_square:] 100%"
                )
                async with aiofiles.open(
                    "shikamaru/txt/funnydomains.txt", mode="r"
                ) as f:
                    domains = await f.readlines()
                async with aiofiles.open(
                    "shikamaru/txt/funnypasswords.txt", mode="r"
                ) as f:
                    passwords = await f.readlines()

                await ctx.reply(
                    f"**Successfully hacked {user}!**\nEmail: `{username.replace('', '') + str(random.randint(20, 99)) + '@' + random.choice(domains)}`Password: `{random.choice(passwords)}`"
                )
        else:
            await ctx.reply("Mention the user you want to hack.")


def load(bot):
    bot.add_plugin(Fun(bot))
