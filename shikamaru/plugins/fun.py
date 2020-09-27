import lightbulb
import hikari
import random
import aiohttp

dog_titles = [
	"Is this Akamaru?",
	"I think Kiba will like this dog",
	"This dog is from the Inuzuka clan",
	"I don't know who this dog is",
	"What a drag dogs are....",
	"Some random dog I found at Naruto's house"
]

class Fun(lightbulb.Plugin):
	def __init__(self, bot):
		super().__init__()
		self.bot = bot

	@lightbulb.command()
	async def dog(self, ctx):
		"""Gives you a random dog."""
		async with aiohttp.ClientSession() as session:
			async with session.get('https://random.dog/woof') as resp:
				if resp.status != 200:
					return await ctx.reply('No dog found :(')
				filename = await resp.text()
				url = f'https://random.dog/{filename}'
				if filename.endswith(('.mp4', '.webm')):
					await ctx.reply("No dogs found \\:(")
				else:
					await ctx.reply(embed=hikari.Embed(title=random.choice(dog_titles), color="#dffc03").set_image(url))

def load(bot):
	bot.add_plugin(Fun(bot))