import datetime
import discord

from dataclasses import dataclass


@dataclass
class MessageDTO:
    author: discord.Member
    created_at: datetime.datetime
    content: str


@dataclass
class FileDTO:
    author: discord.Member
    messages: [MessageDTO]
    channel: discord.TextChannel
