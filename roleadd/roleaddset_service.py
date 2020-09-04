import enum
import discord
from redbot.core.utils.chat_formatting import humanize_list


class AllowOrDeny(enum.Enum):
    ALLOW = 1,
    DENY = 2


class RoleAddSetService:
    def __init__(self, *args, **kwargs):
        self.config = kwargs.get("config")

    async def _get_config_list(self, manager_role: discord.Role, allow_or_deny: AllowOrDeny):
        if allow_or_deny == AllowOrDeny.ALLOW:
            config_setting = self.config.role(manager_role).allowlist()
            title = "Allow list"
        else:
            title = "Deny list"
            config_setting = self.config.role(manager_role).denylist()

        return title, config_setting

    async def append_to_list(self, manager_role: discord.Role, roles: [discord.Role], allow_or_deny: AllowOrDeny) -> discord.Embed:
        title, config_setting = await self._get_config_list(manager_role, allow_or_deny)
        async with config_setting as config_role_list:
            already_existed = []
            appended = []
            for r in roles:
                if r.id not in config_role_list:
                    config_role_list.append(r.id)
                    appended.append(r)
                else:
                    already_existed.append(r)

        embed = discord.Embed(title=f"{title} updated")
        if appended:
            embed.add_field(name="Added", value=humanize_list([str(r) for r in appended]))
        if already_existed:
            embed.add_field(name="Already in list", value=humanize_list([str(r) for r in already_existed]))

        return embed

    async def clear_list(self, manager_role: discord.Role, allow_or_deny: AllowOrDeny) -> discord.Embed:
        title, config_setting = await self._get_config_list(manager_role, allow_or_deny)
        async with config_setting as config_role_list:
            config_role_list = []

        return discord.Embed(title=f"{title} updated", description="All roles have been cleared.")

    async def show_role_list(self, guild: discord.Guild, manager_role: discord.Role, allow_or_deny: AllowOrDeny) -> discord.Embed:
        title, config_setting = await self._get_config_list(manager_role, allow_or_deny)
        roles = await config_setting
        if len(roles) == 0:
            return discord.Embed(title=title, description=f"There are currently no roles for `{manager_role.name}`")

        role_objects = [guild.get_role(r).name for r in roles]

        embed = discord.Embed(
            title=f"{title} roles for {manager_role.name}",
            description=humanize_list(role_objects)
        )
        return embed

    async def remove_role_from_list(self, manager_role: discord.Role, roles_to_remove: [discord.Role], allow_or_deny: AllowOrDeny) -> discord.Embed:
        title, config_setting = await self._get_config_list(manager_role, allow_or_deny)
        async with config_setting as role_list:
            not_in_role_list = []
            removed = []
            for r in roles_to_remove:
                if r.id in role_list:
                    role_list.remove(r.id)
                    removed.append(r)
                else:
                    not_in_role_list.append(r)

        embed = discord.Embed(title=f"{title} updated")
        if removed:
            embed.add_field(name="Removed", value=humanize_list([str(r) for r in removed]))
        if not_in_role_list:
            embed.add_field(name="Not in list", value=humanize_list([str(r) for r in not_in_role_list]))
        if not removed or not_in_role_list:
            embed.description = f"No roles are currently in the allow list for `{manager_role.name}`."

        return embed
