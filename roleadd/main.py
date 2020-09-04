from typing import Sequence

import discord
from discord.ext.commands import Greedy
from redbot.core import checks

from redbot.core.config import Config
from redbot.core.commands import commands
from redbot.core.utils.chat_formatting import humanize_list

from .roleaddset_service import RoleAddSetService, AllowOrDeny

DEFAULT_ROLE = {
    "allowlist": [],
    "denylist": []
}


class RoleAdd(commands.Cog, RoleAddSetService):
    """
    Allow roles to be managed based on currently held roles.
    """
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot
        self.config = Config.get_conf(self, identifier=12903810928309)
        self.config.register_role(**DEFAULT_ROLE)

    @checks.admin_or_permissions(manage_roles=True)
    @commands.group(name="roleaddset")
    async def roleaddset(self, ctx):
        """Settings for role add"""
        pass

    @roleaddset.group("denylist")
    async def denylist(self, ctx):
        """Manage deny list"""
        pass

    @denylist.command(name="add")
    async def _add_to_denylist(self, ctx, manager_role: discord.Role, roles_to_deny: Greedy[discord.Role]):
        """
        Add roles to the deny list for manager role.

        Denying a role allows the manager role to manage all roles, excluding the one's provided.

        `manager_role`
        The role to adjust permissions for.

        `roles_to_allow`
        The roles to allow the manager_role to adjust.
        """
        embed = await self.append_to_list(manager_role, roles_to_deny, AllowOrDeny.DENY)
        return await ctx.send(embed=embed)

    @denylist.command(name="remove", aliases=["del", "delete"])
    async def _remove_role_from_denylist(self, ctx, manager_role: discord.Role, roles_to_remove: Greedy[discord.Role]):
        """Remove role(s) from the denylist for provided manager role."""
        embed = await self.remove_role_from_list(manager_role, roles_to_remove, AllowOrDeny.DENY)
        return await ctx.send(embed=embed)

    @denylist.command(name="show")
    async def _show_denylist_roles(self, ctx, manager_role: discord.Role):
        embed = await self.show_role_list(ctx.guild, manager_role, AllowOrDeny.DENY)
        return await ctx.send(embed=embed)

    @denylist.command(name="clear")
    async def _clear_denylist(self, ctx, manager_role: discord.Role):
        embed = await self.clear_list(manager_role, AllowOrDeny.DENY)
        return await ctx.send(embed=embed)

    @roleaddset.group(name="allowlist")
    async def allowlist(self, ctx):
        """Manage allow list"""
        pass

    @allowlist.command(name="add")
    async def _add_role(self, ctx, manager_role: discord.Role, roles_to_allow: Greedy[discord.Role]):
        """
        Add roles to be allowed to be managed by the manager role.

        Only roles added to this list will be able to be managed by the manager role.
        `manager_role`
        The role to adjust permissions for.

        `roles_to_allow`
        The roles to allow the manager_role to adjust.
        """
        embed = await self.append_to_list(manager_role, roles_to_allow, AllowOrDeny.ALLOW)
        return await ctx.send(embed=embed)

    @allowlist.command(name="remove", aliases=["del", "delete"])
    async def _delete_role_whitelist(self, ctx, manager_role: discord.Role, roles_to_remove: Greedy[discord.Role]):
        """
        Add roles to be allowed to be managed by the manager role.
        `manager_role`
            The role to adjust permissions for.
        `roles_to_remove`
            The roles to allow the manager_role to adjust.
        """
        embed = await self.remove_role_from_list(manager_role, roles_to_remove, AllowOrDeny.ALLOW)
        return await ctx.send(embed=embed)

    @allowlist.command(name="show", aliases=["settings"])
    async def _show_allowlist_roles(self, ctx, manager_role: discord.Role):
        """
        Show allow list roles for specified manager role
        """
        embed = await self.show_role_list(ctx.guild, manager_role, AllowOrDeny.ALLOW)
        return await ctx.send(embed=embed)

    @allowlist.command(name="clear")
    async def _clear_deny_list(self, ctx, manager_role: discord.Role):
        """
        Clear the deny list for the specified manager role
        """
        embed = await self.clear_list(manager_role, AllowOrDeny.ALLOW)
        return await ctx.send(embed=embed)

    @commands.command(name="roleadd")
    async def _add_role(self, ctx, user: discord.Member, role_to_add: discord.Role):
        """
        Add a role to a user.
        """
        all_roles = await self.config.all_roles()
        member_roles = ctx.author.roles

        allowlist = []
        denylist = []
        roles_to_check = [ctx.guild.get_role(role) for role in all_roles if role in [r.id for r in member_roles]]
        for role in roles_to_check:
            allowed = await self.config.role(role).allowlist()
            denied = await self.config.role(role).denylist()

            allowlist.extend(allowed)
            denied.extend(denied)

        try:
            if allowlist and role_to_add.id in allowlist:
                return await user.add_roles(role_to_add, reason=f"Requested by {ctx.author}")

            if denylist and role_to_add.id not in denylist:
                return await user.add_roles(role_to_add, reason=f"Requested by {ctx.author}")
        except discord.errors.Forbidden as e:
            return await ctx.send(f"`{e.text}` - I am unable to add that role.")

        return await ctx.send("You do not have permissions to add that role.")
