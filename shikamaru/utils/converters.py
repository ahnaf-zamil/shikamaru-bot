import typing
import lightbulb
from lightbulb.errors import ConverterFailure
from .code import Code


async def code_converter(arg: lightbulb.WrappedArg) -> Code:
    return Code(arg.data, arg.context)


async def pluginish_converter(arg: lightbulb.WrappedArg) -> typing.Union[lightbulb.Plugin, lightbulb.Group, lightbulb.Command]:
    pluginish = arg.context.bot.get_plugin(arg.data) or arg.context.bot.get_command(
        arg.data
    )
    if not pluginish:
        raise ConverterFailure(f"Failed to get plugin or command with arg {arg}")
    return pluginish


if typing.TYPE_CHECKING:
    code_converter = Code
    pluginish_converter = typing.Union[lightbulb.Plugin, lightbulb.Group, lightbulb.Command]
