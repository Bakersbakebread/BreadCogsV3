import discord

import modmail


async def message(bot, message, config):
    author = message.author
    user_info = await config.user(author).info()

    if user_info["multi_guild_hold"]:
        await author.send(await get_label("info", "guild_react_request"))
        # await author.send(f"{label['handle_messages']['guild_react_request']}")
        return

    if user_info["thread_is_open"]:
        open_thread = bot.get_channel(user_info["thread_id"])
        if open_thread:
            embed = await message_embed(
                message.content, author, is_mod=False, is_anon=False
            )
            await open_thread.send(embed=embed)
            await save_message_to_config(config, author, embed)
            return await message.add_reaction("✅")

    user_is_blocked = await modmail.Modmail.is_user_blocked(author, config)
    if user_is_blocked:
        print(f"[ModMail] Blocked user attempted to message : {author.name}")
        return await author.send(await get_label("errors", "you_are_blocked"))

    # # channel_name = discord.utils.get(self.bot.guilds,
    # id=556800157082058784)

    # Get a list of guilds the user & bot share
    guilds = [
        member.guild for member in bot.get_all_members() if member.id == author.id
    ]

    if len(guilds) > 1:
        async with config.user(author).info() as info:
            info["multi_guild_hold"] = True

        table = [[index, guild.name] for index, guild in enumerate(guilds)]

        await author.send(await get_label("info", "multiple_guilds_ask"))

        msg = await author.send(f"```{tabulate(table, tablefmt='presto')}```")

        emojis = ReactionPredicate.NUMBER_EMOJIS[: len(guilds)]

        start_adding_reactions(msg, emojis)

        pred = ReactionPredicate.with_emojis(emojis, msg)

        await bot.wait_for("reaction_add", check=pred)

        guild = guilds[pred.result]
        await author.send(guild)

    else:
        # guild = bot.get_guild(554733245187751966)
        guild = guilds[0]

    async with config.user(author).info() as user_info:
        # set waiting to True (reset it on reply)
        now = datetime.now()
        try:
            print(f"[ModMail] Attempting to find {author.name} message frequncy")

            user_info["counter"] += 1
            user_info["last_messaged"] = datetime.timestamp(now)
            user_info["thread_is_open"] = True
            user_info["guild_id"] = guild.id
            user_info["multi_guild_hold"] = False

            print(f"[ModMail] {author.name} message frequency: {user_info['counter']}")

        except KeyError:
            print("[ModMail] User not found, created a new entry")

            user_info["counter"] = 1
            user_info["last_messaged"] = datetime.timestamp(now)
            user_info["thread_is_open"] = True
            user_info["guild_id"] = guild.id
            user_info["multi_guild_hold"] = False

    modmail_thread = await channel_finder(author, guild)
    if not modmail_thread:
        # returns False if no permissions to create thread
        modmail_thread = await create.new_modmail_thread(bot, guild, author)
        if not modmail_thread:
            return await author.send(
                await get_label("errors", "no_perms_create_channel")
            )

    async with config.user(author).info() as user_info:
        user_info["thread_id"] = modmail_thread.id

    embed = await message_embed(message.content, author, is_mod=False, is_anon=False)
    await modmail_thread.send(embed=embed)
    await message.add_reaction("✅")
    await save_message_to_config(config, author, embed)