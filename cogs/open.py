import asyncio
import discord
from discord.ext import commands
from discord_slash import SlashContext, cog_ext


class Open(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.slash_say.allowed_guild_ids = [bot.guild_id]
        asyncio.create_task(self.bot.slash.sync_all_commands())

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    @cog_ext.cog_slash(name='open', description='部屋を開いた人以外も自由に閲覧、書き込みできる部屋を開設します。')
    async def slash_say(self, ctx: SlashContext):
        if ctx.channel.id != 836963480069865492:
            return
        channel = await self.bot.category.create_text_channel(name=ctx.author.name)
        msg = await channel.send(f'<@{ctx.author.id}>\nオープンチャンネルを作成しました。')
        url = f'https://discord.com/channels/{self.bot.guild_id}/{channel.id}/{msg.id}'
        embed = discord.Embed(description=f'{channel.mention}')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Open(bot))
