import asyncio

import discord
from discord.ext import commands
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        asyncio.create_task(self.bot.slash.sync_all_commands())
        self.help_em = self.compose_help_em()

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    def compose_help_em(self):
        help_em = [
            (
                discord.Embed(
                    title="個室くんの概要",
                    description="何かのBotです。",
                    color=discord.Colour.blue()
                )
            ),
            (
                discord.Embed(
                    title="OPENコマンド",
                    description="部屋を開いた人以外も自由に閲覧、書き込みできる部屋を開設します。",
                    color=discord.Colour.blue()
                )
            ),
            (
                discord.Embed(
                    title="PRIVATEコマンド",
                    description="管理人・副管理人・権限で許可した人にしか見えなくなる部屋を開設します。",
                    color=discord.Colour.blue()
                )
            )
        ]
        return help_em


    @cog_ext.cog_slash(
        name='help',
        description='このBotのHelpを返します。',
        options=[
            create_option(
                name="command",
                description="helpを表示するコマンドを選択してください。",
                option_type=4, required=False,
                choices=[
                    create_choice(name="open", value=1),
                    create_choice(name="private", value=2)
                ]
            )
        ],
        guild_ids=[self.bot.guild_id]
    )
    async def slash_say(self, ctx: SlashContext, command=None):
        if command is None:
            page = 0
            help_msg = await ctx.send(embed=self.help_em[page])
            emoji = '➡'
            await help_msg.add_reaction(emoji)
            while True:
                def reaction_check(reaction, user):
                    if reaction.message.id == help_msg.id \
                            and user == ctx.author:
                        return reaction, user

                try:
                    reaction, user = await self.bot.wait_for(
                        "reaction_add", timeout=60.0, check=reaction_check)
                    emoji = str(reaction.emoji)
                except asyncio.TimeoutError:
                    await help_msg.remove_reaction(emoji, self.bot.user)
                    return
                if page == len(self.help_em) - 1:
                    page = 0
                else:
                    page += 1
                await help_msg.edit(embed=self.help_em[page])
            return
        elif command == 1:
            await ctx.send(embed=self.help_em[1])
        elif command == 2:
            await ctx.send(embed=self.help_em[2])


def setup(bot):
    bot.add_cog(Help(bot))
