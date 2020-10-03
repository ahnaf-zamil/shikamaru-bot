import lightbulb
import hikari
import aiofiles
import random
import datetime


class Actions(lightbulb.Plugin):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @lightbulb.command()
    async def punch(self, ctx, user=None):
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
    async def run(self, ctx, user=None):
        async with aiofiles.open("shikamaru/txt/run_gifs.txt", mode="r") as f:
            gif_ls = await f.readlines()
        if user != None:
            embed = hikari.Embed(
                title=f"{ctx.message.author} is running away from {user}!",
                color="#852e00",
            )
        else:
            embed = hikari.Embed(
                title=f"{ctx.message.author} is running!", color="#852e00"
            )
        embed.set_footer(text=f"Requested by: {ctx.message.author}")
        embed.set_image(random.choice(gif_ls))
        embed.timestamp = datetime.datetime.now().astimezone()
        await ctx.reply(embed)


def load(bot):
    bot.add_plugin(Actions(bot))