import discord
from tabulate import tabulate

from datetime import datetime

from redbot.core import Config
from redbot.core.utils.menus import start_adding_reactions
from redbot.core.utils.predicates import ReactionPredicate


class MailMessageBase:
    def __init__(self, bot, message):
        self.bot = bot
        self.message: discord.message.Message = message
        self.author = message.author
        print(type(self.author))

        self.config = Config.get_conf(cog_instance=self.bot.get_cog(name="Modmail"), identifier=2807305259608965131)
        print(type(self.config))


class UserToModMessage(MailMessageBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.guild = None
        self.channel = None
        self.shared_guilds = [
            member.guild for member in self.bot.get_all_members() if member.id == self.author.id
        ]

    async def get_user_config(self):
        """
        Helper to get user info
        """
        x = await self.config.user(self.author).info()
        return x

    async def is_user_blocked(self) -> bool:
        """
        Checks whether is allowed to send messages
        :return: Bool
        """
        # maybe move this to user config?
        async with self.config.blocked() as blocked:
            if self.author.id in blocked:
                return True
            else:
                return False

    async def is_active_thread(self):
        """
        Checks if modmail message/thread is already in progress
        :return: None
        """

        user_config = await self.get_user_config()
        try:
            if user_config['multi_guild_hold']:
                await self.author.send("Already waiting for your answer")

            if user_config.get("thread_is_open"):
                open_thread = self.bot.get_channel(user_config["thread_id"])
                if open_thread:
                    self.channel = open_thread
                    print("send to channel")
                    pass
        except:
            pass

    async def shared_guilds_check(self) -> discord.guild.TextChannel:
        """
        Sends Embed Reaction table to determine where to send modmail message
        """
        user_info = await self.config.user(self.author).info()
        print(user_info)
        async with self.config.user(self.author).info() as info:
            info["multi_guild_hold"] = True

        table = [
            [index, guild.name] for index, guild in enumerate(self.shared_guilds)
        ]
        # await self.author.send(await get_label("info", "multiple_guilds_ask"))
        await self.author.send("More than one guild:")
        msg = await self.author.send(f"```{tabulate(table, tablefmt='presto')}```")

        emojis = ReactionPredicate.NUMBER_EMOJIS[: len(self.shared_guilds)]
        start_adding_reactions(msg, emojis)
        pred = ReactionPredicate.with_emojis(emojis, msg)

        await self.bot.wait_for("reaction_add", check=pred)

        await self.author.send(self.guild)
        return self.shared_guilds[pred.result]

    async def send_modmail_message(self):
        # check if blocked
        if await self.is_user_blocked():
            return print("User is blocked")

        # check if thread is open
        if await self.is_active_thread():
            return print("Send to channel")

        # multi-guild checker
        if len(self.shared_guilds) > 1:
            self.guild = await self.shared_guilds_check()
        else:
            # well, there's only one guild right?
            self.guild = self.shared_guilds[0]

        async with self.config.user(self.author).info() as user_config:
            now = datetime.now()
            user_config = {
                "counter": +1,
                "last_messaged": datetime.timestamp(now),
                "thread_is_open": True,
                "guild_id": self.guild.id,
                "multi_guild_hold": False
            }
        await self.author.send('TEST')





