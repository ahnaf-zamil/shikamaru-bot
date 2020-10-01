import asyncio
import inspect
from datetime import datetime, timezone
from random import randint
import io
import hikari
import lightbulb
from lightbulb import Context, WrappedArg, checks, commands, text_channel_converter
from lightbulb.errors import NotOwner
from lightbulb.utils import EmbedNavigator, EmbedPaginator
from shikamaru.utils.converters import code_converter, pluginish_converter
import sys
import platform
import textwrap
import traceback
import time
from contextlib import redirect_stdout


class SuperUser(lightbulb.Plugin):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    def eprint(self, *args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)

    @checks.owner_only()
    @lightbulb.command(aliases=["exec", "eval"])
    async def code(self, ctx) -> None:
        start = time.monotonic()
        command = ctx.message.content[:7]
        channel = self.bot.cache.get_guild_channel(ctx.message.channel_id)
        code = ctx.message.content[len(command) + 1 :]
        await self.bot.rest.trigger_typing(channel)
        if code.startswith("```") and code.endswith("```"):
            code = "\n".join(code.split("\n")[1:-1])
        else:
            code = code.strip("` \n")
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
            "ctx": ctx,
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
                colour=(255, 10, 40),
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
                colour=(255, 10, 40),
            )
            await ctx.reply(embed=embed)
            await ctx.message.add_reaction("❌")
            return
        value = stdout.getvalue()
        millis = (time.monotonic() - start) * 1000
        em = hikari.Embed(
            title=f"Executed in {int(millis):,.2f}ms",
            description=f"\n\nStdout:\n```py\n# Python {platform.python_version()} - Hikari {hikari.__version__} - lightbulb {lightbulb.__version__} \n\n{value if value != '' else None}```\nReturned:\n```py\n{result}\n```",
            color=(40, 255, 10),
        )
        await ctx.message.add_reaction("✅")
        await ctx.reply(embed=em)

    @checks.owner_only()
    @commands.command(aliases=["rst"])
    async def restart(self, ctx):
        await ctx.reply("Ja, matane")
        asyncio.create_task(self.bot.close())

    @checks.owner_only()
    @commands.command(aliases=["showcode", "codefor", "source"])
    async def getcode(self, ctx: Context, child: pluginish_converter):
        body = (
            inspect.getsource(child.__class__)
            if isinstance(child, lightbulb.Plugin)
            else inspect.getsource(child._callback)
        )
        paginator = EmbedPaginator(prefix="```py\n", suffix="```", max_lines=20)

        @paginator.embed_factory()
        def make_embed(index, page):
            return hikari.Embed(
                title=f"Code for {child.name}",
                description=page,
                colour=randint(0, 0xFFF),
                timestamp=datetime.now(tz=timezone.utc),
            ).set_footer(
                text=f"{index}/{len(paginator)}",
                icon=ctx.author.avatar_url,
            )

        paginator.add_line(body.replace("`", "ˋ"))
        navigator = EmbedNavigator(paginator.build_pages())
        await navigator.run(ctx)

    @checks.owner_only()
    @commands.command(name="selfclean", aliases=["sclean", "sclear"])
    async def self_clean(self, ctx: Context, amount: int = 30):
        # noinspection PyTypeChecker
        channel: hikari.TextChannel = context.bot.cache.get_guild_channel(
            ctx.channel_id
        ) or await ctx.bot.rest.fetch_channel(ctx.channel_id)

        history = (
            channel.history(before=ctx.message_id)
            .filter(lambda m: m.author.id == ctx.bot.me.id)
            .limit(amount)
        )

        if not isinstance(channel, hikari.DMChannel):
            await self.bot.rest.delete_messages(channel, *(await history))
        else:
            async for message in history:
                await message.delete()


def load(bot):
    bot.add_plugin(SuperUser(bot))
