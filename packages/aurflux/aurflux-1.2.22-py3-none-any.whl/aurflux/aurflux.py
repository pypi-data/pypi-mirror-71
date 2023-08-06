from __future__ import annotations


import discord.errors
import traceback
import abc
from .command import Command, CommandCheck
from .config import Config
from .context import MessageContext
from .errors import *
from .response import Response
from . import utils
from . import argh
import re
from aurcore.event import *

if ty.TYPE_CHECKING:
    import discord
    from ._types import *


class AurfluxEvent(Event):
    def __init__(self, aurflux, __event_name, *args, **kwargs):
        super().__init__(__event_name, *args, **kwargs)
        self.bot: Aurflux = aurflux
class AurfluxCog:
    def __init__(self, aurflux: Aurflux):
        self.aurflux = aurflux
        self.router = EventRouter(self.__class__.__name__, self.aurflux.router)
        self.route()

    @abc.abstractmethod
    def route(self): ...


def __aiterify(obj: ty.Union[ty.Coroutine, ty.AsyncIterable]):
    if asyncio.iscoroutine(obj) or asyncio.isfuture(obj):
        class AiterCoro:
            def __aiter__(self):
                async def gen():
                    yield await obj

                return gen()

        return AiterCoro()
    else:
        return obj


def register_builtins(aurflux: Aurflux):
    @aurflux.router.endpoint(":ready", decompose=True)
    async def _():
        print("Ready!")

    @aurflux.router.endpoint(":message", decompose=True)
    async def command_listener(message: discord.Message):
        if not message.content or message.author is aurflux.user:
            return

        ctx = MessageContext(bot=aurflux, message=message)
        prefix = aurflux.CONFIG.of(ctx)["prefix"]
        cmd = message.content.split(" ", 1)[0][len(prefix):]

        if cmd not in aurflux.commands:
            return

        if not message.content.startswith(prefix):
            return
        try:
            if cmd not in aurflux.commands:
                return
            async with ctx.channel.typing():
                async for response in __aiterify(aurflux.commands[cmd].execute(ctx)):
                    await response.execute(ctx)
        except CommandError as e:
            info_message = f"{e}"
            if argparser := aurflux.commands[cmd].argparser:
                info_message += f"\n```{argparser.format_help()}```"
            await Response(content=info_message, errored=True).execute(ctx)
        except CommandInfo as e:
            info_message = f"{e}"
            if argparser := aurflux.commands[cmd].argparser:
                info_message += f"\n```{argparser.format_help()}```"
            await Response(content=info_message).execute(ctx)

    @CommandCheck.check(lambda ctx: ctx.author.id == aurflux.admin_id)
    @aurflux.commandeer(name="exec", parsed=False, private=True)
    async def exec_(ctx: MessageContext, script: str):
        exec_func = utils.sexec
        if any(line.strip().startswith("await") for line in script.split("\n")):
            exec_func = utils.aexec

        with utils.Timer() as t:
            # noinspection PyBroadException
            try:
                res = await exec_func(script, globals(), locals())
            except Exception as e:
                res = re.sub(r'File ".*[\\/]([^\\/]+.py)"', r'File "\1"', traceback.format_exc(limit=1))
        return Response((f""
                         f"Ran in {t.elapsed * 1000:.2f} ms\n"
                         f"**IN**:\n"
                         f"```py\n{script}\n```\n"
                         f"**OUT**:\n"
                         f"```py\n{res}\n```"), trashable=True)

    @aurflux.commandeer(name="help", parsed=False)
    async def get_help(ctx: MessageContext, help_target: ty.Optional[str]):
        """
        help [command_name]
        :param ctx:
        :param args:
        :return:
        """
        configs = aurflux.CONFIG.of(ctx)
        public_cmds = {name: command for name, command in aurflux.commands.items() if not command.private and name != "help"}
        if not help_target:
            help_embed = discord.Embed(title=f"{utils.EMOJIS['question']} Command Help", description=f"{configs['prefix']}help <command> for more info")
            for cmd_name, command in public_cmds.items():
                help_embed.add_field(name=cmd_name, value=f"{configs['prefix']}{command.short_usage}", inline=False)

            return Response(
                embed=help_embed
            )
        else:
            if help_target not in public_cmds:
                return Response(f"No command `{help_target}` to show help for", errored=True)
            embed = discord.Embed(
                title="\U00002754 Command Help",
                description=f"Help for `{configs['prefix']}{help_target}`")
            if public_cmds[help_target].argparser:
                embed.add_field(name="Usage", value=public_cmds[help_target].long_usage)
            return Response(embed=embed)

class Aurflux(discord.Client):
    CONFIG: Config

    def __init__(self, name, admin_id: int, parent_router: EventRouter = None, *args, **kwargs):
        super(Aurflux, self).__init__(*args, **kwargs)
        self.CONFIG = Config(name)
        self.commands: ty.Dict[str, Command] = {}
        self.router = EventRouter(name="aurflux", parent=parent_router)
        self.admin_id = admin_id
        register_builtins(self)

    def commandeer(self, name: ty.Optional[str] = None, parsed: bool = True, private: bool = False) -> ty.Callable[[ty.Callable[[...], ty.Awaitable[Response]]], Command]:
        def command_deco(func: ty.Callable[[...], ty.Awaitable[Response]]) -> Command:
            cmd = Command(client=self, func=func, name=(name or func.__name__), parsed=parsed, private=private)
            if cmd.name in self.commands:
                raise TypeError(f"Attempting to register command {cmd} when {self.commands[cmd.name]} already exists")
            self.commands[cmd.name] = cmd
            return cmd

        return command_deco

    def dispatch(self, event, *args, **kwargs):
        super(Aurflux, self).dispatch(event, *args, **kwargs)
        asyncio.create_task(self.router.submit(AurfluxEvent(self, f":{event}", *args, **kwargs)))

    def register_cog(self, cog: ty.Type[AurfluxCog]):
        cog(self)




