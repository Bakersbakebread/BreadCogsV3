import datetime
import discord
import logging

from redbot.core.commands import commands
from redbot.core.data_manager import bundled_data_path

from .models import FileDTO, MessageDTO

FILENAME = "channelarchive.md"
TEN_DASH = "-" * 10

log = logging.getLogger(name="red.breadcogs.channelarchive")


class ChannelArchive(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot
        self.data_path = bundled_data_path(self)

    async def make_nice_file(self, data: FileDTO) -> None:
        with open(f"{self.data_path}/{FILENAME}", "w", encoding="utf-8") as f:
            f.write(f"# {data.channel} | {data.channel.id}\n\n")
            f.write("Date Archived (UTC)\n")
            f.write(f"> {datetime.datetime.utcnow()}\n\n")
            f.write(f"By whom\n")
            f.write(f"> {data.author} (`{data.author.id}`)\n\n")
            f.write(f"Total messages\n")
            f.write(f"> {len(data.messages)}\n\n")
            f.write("---\n")
            for message_dto in data.messages:
                f.write(f"\n#### {message_dto.author} - `{message_dto.author.id}`\n")
                f.write(f"{message_dto.content}\n\n")
                f.write(f"`Timestamp: {message_dto.created_at}`\n")
            f.write(TEN_DASH)

    @commands.command(name="archive")
    async def _archive_channel(self, ctx, channel: discord.TextChannel = None, target: discord.TextChannel = None):
        """
        Archive a channel into a text file, this will probably fail at larger channels!

        Example:
            [p]archive #channel_I_want_archiving #to_the_channel
        """
        channel = channel if channel else ctx.channel
        target = target if target else ctx.channel
        messages = []

        def transform(m):
            return MessageDTO(author=m.author, created_at=m.created_at, content=m.content)

        count = 0
        help_message = await ctx.send(f"🔍 Collecting messages...")
        async for message in channel.history(limit=50000).map(transform):
            messages.append(message)
            count += 1
            log.debug(f"{count} - Appended")

        file_dto = FileDTO(author=ctx.author, messages=messages, channel=channel)
        await self.make_nice_file(file_dto)
        await help_message.delete()
        try:
            await target.send(f"Channel archive: {channel} `{channel.id}`.", file=discord.File(f"{self.data_path}/{FILENAME}"))
        except discord.errors.Forbidden:
            return await ctx.send("Missing permissions to send message.")
        except discord.errors.HTTPException:
            return await ctx.send("File is too large to send.")
