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
	        code = ctx.message.content[len(command) + 1:]

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
	            exec(new_forced_async_code, env) # shut up pylint with "[exec-used] Use of exec [W0122]"
	        except Exception as error: # shut up pylint with "[broad-except] Catching too general exception Exception [W0703]"
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
	        except Exception as error: # shut up pylint with "[broad-except] Catching too general exception Exception [W0703]"
	            value = stdout.getvalue()
	            embed = hikari.Embed(
	                title="Failed to execute.",
	                description=f"{error} ```py\n{traceback.format_exc()}\n```\n```py\n{value}\n```",
	                colour=(255, 10, 40)
	            )
	            await ctx.reply(embed=embed)
	            await ctx.message.add_reaction("❌")
	            return

	        value = stdout.getvalue()
	        embed = hikari.Embed(
	            title="Success!",
	            description=f"Returned value: ```py\n{result}\n```\nStandard Output: ```py\n{value}\n```",
	            colour=(5, 255, 70)
	        )
	        await ctx.reply(embed=embed)
	        await ctx.message.add_reaction("✅")

def load(bot):
	bot.add_plugin(Owner(bot))