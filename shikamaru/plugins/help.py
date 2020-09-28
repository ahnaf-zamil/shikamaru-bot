import lightbulb
import hikari
import datetime
from lightbulb import help

class CustomHelp(help.HelpCommand):
    # Using lightbulb's auto-generated help command
    # Just need to override the methods

    def __init__(self, bot):
        self.bot = bot
        self.type_name_map = {'int': 'number', 'str': 'text', 'float': 'decimal'}

    async def object_not_found(self, ctx, name):
        pass

    async def send_help_overview(self, ctx):
        em = hikari.Embed(title="Shikamaru Help", description="Shikamaru is an open-source Discord bot filled with numerous features.\n Type sh!help <command name> to get info about a specific command.")
        em.set_thumbnail(image=self.bot.me.avatar_url)
        #for i in self.bot.commands:

        await ctx.reply("Unfinished help command")

    async def send_plugin_help(self, ctx, plugin):
        pass

    async def send_command_help(self, ctx, command):

        em = hikari.Embed(title=f"Help for: {command.name.capitalize()}", color="#ae00ff" )
        # ({self.type_name_map[command.arg_details.args[i].annotation.__name__]})
        command_name = ctx.prefix + command.name
        arg_list = [i for i in command.arg_details.args if i not in ['self', 'ctx']]
        em.description = f"**Name:** {command.name}\n**Description:**{help.get_help_text(command)}\n**Usage:** `{command_name} {' '.join(arg_list)}`"
        em.set_footer(text=f"Requested by: {ctx.message.author}", icon=ctx.message.author.avatar_url)
        em.timestamp = datetime.datetime.now().astimezone()
        await ctx.reply(embed=em)

    async def send_group_help(self, ctx, group):
        pass

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
