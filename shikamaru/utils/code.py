import asyncio
import contextlib
import io
import logging
import platform
import re
import textwrap
import traceback
import typing
from datetime import datetime, timezone

import hikari
import lightbulb
from lightbulb import Context
from lightbulb.utils import EmbedNavigator, EmbedPaginator


# noinspection PyProtectedMember
class Code:
    PATTERN = re.compile(r"```(?P<syntax>.*)\n(?P<body>[^`]+?)```")

    @staticmethod
    def clean(body):
        match = Code.PATTERN.search(body)
        return match.groups() if match else (None, body)

    @staticmethod
    def get_syntax_error(error: SyntaxError) -> str:
        """return syntax error string from error"""
        if error.text is None:
            return f"{error.__class__.__name__}: {error}\n"
        return f'{error.text}{"^":>{error.offset}}\n{type(error).__name__}: {error}'

    @staticmethod
    def wrap(body):
        return "async def __invoke__(bot):\n" + textwrap.indent(body, " " * 4)

    async def _execute(self):
        start = datetime.now(tz=timezone.utc)
        stack = contextlib.AsyncExitStack()
        stream = io.StringIO()
        stack.enter_context(contextlib.redirect_stdout(stream))
        stack.enter_context(contextlib.redirect_stderr(stream))
        stream_handler = logging.StreamHandler(stream)

        if logger := getattr(self.context.command.plugin, "logger"):
            logger.addHandler(stream_handler)

        async with stack:
            try:
                env: typing.Dict[str, typing.Any] = {
                    "self": self.context.command.plugin,
                    "ctx": self.context,
                    "context": self.context,
                    "channel": self.context.channel,
                    "channel_id": self.context.channel_id,
                    "author": self.context.member or self.context.author,
                    "guild": self.context.guild,
                    "guild_id": self.context.guild_id,
                    "message": self.context.message,
                    "_": getattr(self.context.command.plugin, "last_result", None),
                }
                env.update(globals())
                env.update(locals())
                exec(str(self), env)
                func = env["__invoke__"]
                res = await func(self.context.bot)
                setattr(self.context.command.plugin, "last_result", res)
                print(f"- Returned {res}")
            except SyntaxError as e:
                print(self.get_syntax_error(e))
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
            else:
                self.success = True
        if logger:
            logger.removeHandler(stream_handler)

        stream.seek(0)
        lines = (
            "\n".join(stream.readlines())
            .replace(self.context.bot._token, "~TOKEN~")
            .replace("`", "´")
        )
        paginator = EmbedPaginator(
            max_lines=27, prefix="```diff\n", suffix="```", max_chars=1048
        )

        @paginator.embed_factory()
        def make_page(index, page):
            return hikari.Embed(
                title=f"Executed in {(datetime.now(tz=timezone.utc) - start).total_seconds() * 1000:.2f}ms",
                colour=0x58EF92 if self.success else 0xE74C3C,
                description=f"Result: {page}",
                timestamp=datetime.now(tz=timezone.utc),
            ).set_footer(
                text=f"Page {index}/{len(paginator)}",
                icon=self.context.author.avatar_url,
            )

        paginator.add_line(
            f"*** Python {platform.python_version()} - Hikari {hikari.__version__} - lightbulb {lightbulb.__version__}\n"
            + lines
        )

        navigator = EmbedNavigator(pages=paginator.build_pages())
        await navigator.run(self.context)

    async def _shell(self):
        start = datetime.now(tz=timezone.utc)
        stack = contextlib.AsyncExitStack()
        stream = io.StringIO()
        stack.enter_context(contextlib.redirect_stdout(stream))
        stack.enter_context(contextlib.redirect_stderr(stream))

        async with stack:
            process = await asyncio.create_subprocess_shell(
                self.code,
            )
            await process.communicate()
            print(f"\n- Return code {process.returncode}")

        lines = (
            "\n".join(stream.readlines())
            .replace(self.context.bot._token, "~TOKEN~")
            .replace("`", "´")
        )

        paginator = EmbedPaginator(
            max_lines=27, prefix="```diff\n", suffix="```", max_chars=1048
        )

        @paginator.embed_factory()
        def make_page(index, page):
            return hikari.Embed(
                title=f"Executed in {(datetime.now(tz=timezone.utc) - start).total_seconds() * 1000:.2f}ms",
                colour=0x58EF92 if process.returncode == 0 else 0xE74C3C,
                description=f"Result: {page}",
                timestamp=datetime.now(tz=timezone.utc),
            ).set_footer(
                text=f"Page {index}/{len(paginator)}",
                icon=self.context.author.avatar_url,
            )

        paginator.add_line(
            f"*** Python {platform.python_version()} - Hikari {hikari.__version__} - lightbulb {lightbulb.__version__}\n"
            + lines
        )

        navigator = EmbedNavigator(pages=paginator.build_pages())
        await navigator.run(self.context)

    def __init__(self, code: str, context: Context):
        self.context = context
        self.original = code
        self.language, code = self.clean(code)
        self.code = self.wrap(code)
        self.success = False
        self.run: typing.Callable[[], typing.Coroutine] = (
            self._shell
            if self.context.invoked_with in ("sh", "shell")
            else self._execute
        )

    def __str__(self):
        return self.code

    def __repr__(self):
        return self.original
