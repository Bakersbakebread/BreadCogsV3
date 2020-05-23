import discord
import random
import asyncio
import logging

from typing import Optional, Dict, List, Any, Union
from redbot.core.commands import commands
from redbot.core.data_manager import bundled_data_path
from redbot.core.utils.chat_formatting import pagify

log = logging.getLogger(name="red.breadcogs.randomword")

LEET: Dict[str, List[str]] = {
    "a": ["4", "@"],
    "b": ["8",],
    "c": ["(",],
    "e": ["3",],
    "f": ["ph", "pH"],
    "g": ["9", "6"],
    "h": ["#",],
    "i": ["1", "!", "|"],
    "l": ["!", "|"],
    "o": ["0", "()"],
    "q": ["kw",],
    "s": ["5", "$"],
    "t": ["7",],
    "x": ["><",],
    "y": ["j",],
    "z": ["2",],
}

LEET_SHORT: Dict[str, str] = {
    "a": "4",
    "b": "8",
    "e": "3",
    "g": "6",
    "i": "1",
    "o": "0",
    "s": "5",
    "t": "7",
    "z": "2",
}


class RandomWord(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_path = bundled_data_path(self)
        self.adjectives: List[str] = []
        self.nouns: List[str] = []
        self.verbs: List[str] = []
        asyncio.create_task(self.register_words())

    async def register_words(self) -> None:
        """
        Get's words from cog data path and saves them to an instance var.
        """
        with open(f"{self.data_path}/adjectives.txt") as f:
            adjectives = [line.rstrip() for line in f]
            self.adjectives = adjectives

        with open(f"{self.data_path}/verbs.txt") as f:
            verbs = [line.rstrip() for line in f]
            self.verbs = verbs

        with open(f"{self.data_path}/nouns.txt") as f:
            nouns = [line.rstrip() for line in f]
            self.nouns = nouns

    @staticmethod
    def mini_leet_word(word: str) -> str:
        leeted_word = ""
        for char in word:
            char_copy = char.lower()
            if char_copy in LEET_SHORT:
                char = LEET_SHORT[char_copy]

            leeted_word += char

        return leeted_word

    @staticmethod
    def long_leet_word(word: str) -> str:
        leeted_word = ""
        for char in word:
            char_copy = char.lower()
            if char_copy in LEET:
                if random.random() > 0.8:  # NOT EXACTLY 80% - I'm sorry Mom
                    char = random.choice(LEET[char_copy])
            else:
                if random.random() < 0.2:  # NOT EXACTLY 20%
                    char = char.upper()
            leeted_word += char

        return leeted_word

    @commands.command(name="leetword")
    async def _leet_word(self, ctx, *, words: str):
        """L33T a word, or words."""
        words = [self.long_leet_word(word) for word in words]
        await ctx.send(" ".join(words))

    @commands.command(name="leetmember", aliases=["leetmem", "leetmemb"])
    async def _leet_member(self, ctx, member: discord.Member = None):
        """L33T a Member's name!"""
        member = ctx.author if member is None else member
        to_change = member.nick if member.nick else member.name

        await ctx.send(self.long_leet_word(to_change))

    @commands.group(name="randomword", aliases=["rword", "notexactlyrandomword"])
    async def _random_word(self, ctx):
        """Make a random word!"""

    @_random_word.command(name="verb")
    async def _random_verb(self, ctx):
        """Get a random verb!"""
        await ctx.send(random.choice(self.verbs))

    @_random_word.command(name="adjective")
    async def _random_adjective(self, ctx):
        """Get a random adjective!"""
        await ctx.send(random.choice(self.adjectives))

    @_random_word.command(name="noun")
    async def _random_noun(self, ctx):
        """Get a random noun!"""
        await ctx.send(random.choice(self.nouns))

    @_random_word.command(name="leet")
    async def _random_leet_word(self, ctx, short_leet: Optional[bool] = False, length: int = 1):
        """Get a random leeted word, or words!"""
        if length > 10000:
            return await ctx.send(":expressionless:")
        if length > 100:
            return await ctx.send("Please choose a length less than 100.")
        all_words = self.adjectives + self.nouns + self.verbs
        random.shuffle(all_words)
        if short_leet:
            all_words_leeted = [self.mini_leet_word(word) for word in all_words]
        else:
            all_words_leeted = [self.long_leet_word(word) for word in all_words]

        for p in pagify(" ".join(all_words_leeted[:length])):
            await ctx.send(p)

    @_random_word.command(name="brand")
    async def _random_brand_name(self, ctx, member: discord.Member = None):
        """Find a random brand name!

        Pass a member to rename them!
        """
        adjective = random.choice(self.adjectives)
        verb = random.choice(self.verbs)
        noun = random.choice(self.nouns)
        brand_name = f"{verb.title()} {adjective.title()} {noun.title()}"
        try:
            await ctx.send(f"{brand_name}™")
        except discord.errors.Forbidden:
            log.warning(f"[BrandName] Failed to send message due to missing permissions.")

        if member:
            try:
                await member.edit(nick=brand_name, reason="Brand name changer")
            except discord.errors.Forbidden:
                log.warning(f"Could not edit member's nick due to missing permissions.")
