import lightbulb
from lightbulb import help

class CustomHelp(help.HelpCommand):
    # Using lightbulb's auto-generated help command
    # Just need to override the methods

    async def object_not_found(self, context, name):
        pass

    async def send_help_overview(self, context):
        print("Unfinished help command")

    async def send_plugin_help(self, context, plugin):
        pass

    async def send_command_help(self, context, command):
        pass

    async def send_group_help(self, context, group):
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
