import lightbulb
import hikari
import io
import sys
import textwrap
import traceback
from contextlib import redirect_stdout

command = "sh!code"

class Owner(lightbulb.Plugin):

	def __init__(self, bot):
		super().__init__()
		self.bot = bot

	def eprint(self, *args, **kwargs):
		print(*args, file=sys.stderr, **kwargs)

	@lightbulb.command()
	async def code(self, ctx) -> None:
		if str(ctx.message.author.id) in self.bot.owner_ids:
			channel = self.bot.cache.get_guild_channel(ctx.message.channel_id)
			code = ctx.message.content[len(command) + 1:]
			await self.bot.rest.trigger_typing(channel)
			if code.startswith('```') and code.endswith('```'):
			    code = '\n'.join(code.split('\n')[1:-1])
			else:
				code = code.strip('` \n')
			env = {
				"bot": self.bot,
				"client": self.bot,
				"msg": ctx.message,
				"message": ctx.message,
				"server_id": ctx.message.guild_id,
				"guild_id": ctx.message.guild_id,
				"channel_id": ctx.message.channel_id,
				"author": ctx.message.author,
				"eprint": self.eprint,
				"ctx": ctx
			}
			env.update(globals())
			stdout = io.StringIO()
			new_forced_async_code = f"async def code():\n{textwrap.indent(code, '    ')}"
			try:
				exec(new_forced_async_code, env)
			except Exception as error:
				embed = hikari.Embed(
					title="Failed to execute.",
					description=f"{error} ```py\n{traceback.format_exc()}\n```\n```py\n{error.__class__.__name__}\n```",
					colour=(255, 10, 40)
				)
				await ctx.reply(embed=embed)
				await ctx.message.add_reaction("❌")
				return
			code = env["code"]
			try:
				with redirect_stdout(stdout):
					result = await code()
			except Exception as error:
				value = stdout.getvalue()
				embed = hikari.Embed(
					title="Failed to execute.",
					description=f"{error} ```py\n{traceback.format_exc()}\n```",
					colour=(255, 10, 40)
				)
				await ctx.reply(embed=embed)
				await ctx.message.add_reaction("❌")
				return
			value = stdout.getvalue()
			em = hikari.Embed(
				title="Output",
				description=f"```py\n{result}\n```",
				color=(40, 255, 10)
			)
			await ctx.reply(embed=em)
			await ctx.message.add_reaction("✅")

def load(bot):
	bot.add_plugin(Owner(bot))
