import discord
import random

from discord.ext.commands import Greedy
from redbot.core.commands import commands


class TeamShuffle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def shuffle_partition(l: [], n: int) -> []:
        """Util method to copy the original list, shuffle it and part into n chunks"""
        copy = l[:]
        random.shuffle(copy)
        return [copy[i::n] for i in range(n)]

    @staticmethod
    def build_embed(shuffle_sorted):
        embed = discord.Embed()
        for index, team in enumerate(shuffle_sorted, 1):
            mem = [m.mention for m in team]
            embed.add_field(name=f"**Group {index}**", value="\n".join(mem))

        return embed

    @commands.group(name="teamshuffle", aliases=["teamsort"])
    async def _team_shuffle(self, ctx):
        """
        Sort based on Voice Channel, or Members!
        """

    @_team_shuffle.command(name="member")
    async def _shuffle_members(self, ctx, members: Greedy[discord.Member], groups: int = 2):
        """
        Sort members into lists!

        This default to 2 lists
        """
        if len(members) == 1:
            return await ctx.send("There needs to be at least two members to sort into groups.")

        shuffle_sorted = self.shuffle_partition(members, groups)
        embed = self.build_embed(shuffle_sorted)

        await ctx.send(embed=embed)

    @_team_shuffle.command(name="voice")
    async def _voice_shuffle(self, ctx, channel: discord.VoiceChannel = None, groups: int = 2):
        """Sort members into lists, default is two that in a voice channel!"""
        if channel is None:
            if not ctx.author.voice:
                return await ctx.send("You need to join a voice channel first!")
            else:
                channel = ctx.author.voice.channel

        members = [mem for mem in channel.members if not mem.bot]
        if len(members) == 0:
            return await ctx.send("There are no members inside that voice channel.")
        if len(members) == 1:
            return await ctx.send("There needs to be at least two members to sort into groups.")

        shuffle_sorted = self.shuffle_partition(members, groups)
        embed = self.build_embed(shuffle_sorted)

        await ctx.send(embed=embed)
