import asyncio
import discord
from discord.ext import commands
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option


class Edit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.slash_say.allowed_guild_ids = [bot.guild_id]
        asyncio.create_task(self.bot.slash.sync_all_commands())

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    @cog_ext.cog_slash(
        name='edit',
        description='チャンネルの編集をします',
        options=[
            create_option(
                name="target",
                description="編集する項目を選択してください。",
                option_type=4, required=True,
                choices=[
                    create_choice(name="チャンネル名", value=1)
                ]
            ),
            create_option(
                name="element",
                description="名前を入力してください",
                option_type=3, required=True
            )
        ]
    )
    async def slash_say(self, ctx: SlashContext, target, element):
        msg = (await ctx.channel.history(limit=1, oldest_first=True).flatten())[0]
        if str(ctx.author.id) not in msg.content:
            embed = discord.Embed(title='ERROR', description='他の人が作成したチャンネルを編集することはできません。')
            return await ctx.send(embed=embed)
        if target == 1:
            await ctx.channel.edit(name=element)
            embed = discord.Embed(description=f'チャンネル名を{ctx.channel.mention}に変更しました')
            return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Edit(bot))
