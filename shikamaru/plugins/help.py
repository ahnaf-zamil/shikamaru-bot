import lightbulb
import hikari
import datetime
from lightbulb import help


class CustomHelp(help.HelpCommand):
    # Using lightbulb's auto-generated help command
    # Just need to override the methods

    def __init__(self, bot):
        self.bot = bot

    async def object_not_found(self, ctx, name):
        await ctx.reply(f"Command/Category not found for **{name}**.")

    async def send_help_overview(self, ctx):
        em = hikari.Embed(
            title=f"{self.bot.me.username}'s Help Command",
            color="#32a89d",
            description=f"{self.bot.me.username} is an open-source Discord bot filled with numerous features.\nThe bot prefix is `{self.bot.prefix}`.\nType `{self.bot.prefix}help <command name>` to get info about a specific command.",
        )
        em.set_author(name=str(ctx.message.author), icon=ctx.message.author.avatar_url)
        em.set_thumbnail(self.bot.me.avatar_url)
        plglist = self.bot.plugins
        for plugin in plglist:
            if plugin in self.bot.hidden_plugins:
                continue
            commands = ""
            for i in list(self.bot.get_plugin(plugin).commands):
                commands += f"`{i.replace(' ', '')}`, "
            em.add_field(name=str(plugin), value=commands[:-2])
        em.set_footer(
            text=f"Requested by: {ctx.message.author}",
            icon=ctx.message.author.avatar_url,
        )
        em.timestamp = datetime.datetime.now().astimezone()
        await ctx.reply(embed=em)

    async def send_plugin_help(self, ctx, plugin):

        if plugin.name in self.bot.hidden_plugins:
            await self.object_not_found(ctx, plugin.name)
            return
        commands = ""
        for i in list(plugin.commands):
            commands += f"`{i.replace(' ', '')}`, "
        em = hikari.Embed(
            title=f"Help for: {plugin.name}", color="#ffc400", description=commands[:-2]
        )
        em.set_footer(
            text=f"Requested by: {ctx.message.author}",
            icon=ctx.message.author.avatar_url,
        )
        em.timestamp = datetime.datetime.now().astimezone()
        await ctx.reply(embed=em)

    async def send_command_help(self, ctx, command):

        em = hikari.Embed(
            title=f"Help for: {command.name.capitalize()}", color="#ae00ff"
        )
        command_name = ctx.prefix + command.name
        arg_list = [
            f"<{i}>" for i in command.arg_details.args if i not in ["self", "ctx"]
        ]
        usage = f"{command_name} {' '.join(arg_list)}"
        em.description = f"**Name:** {command.name}\n**Description: **{help.get_help_text(command)}\n**Category:** {command.plugin.name}\n**Usage:** `{usage[:len(list(usage))-1] if not usage.endswith('>') else usage}`" # Removing the last space from the command after joining args with spaces
        em.set_footer(
            text=f"Requested by: {ctx.message.author}",
            icon=ctx.message.author.avatar_url,
        )
        em.timestamp = datetime.datetime.now().astimezone()
        await ctx.reply(embed=em)


class Help(lightbulb.Plugin):
    # Help command plugin

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self._original_help_command = bot.help_command
        bot.help_command = CustomHelp(bot)

    def plugin_remove(self):
        self.bot.help_command = self._original_help_command


def load(bot):
    bot.add_plugin(Help(bot))
