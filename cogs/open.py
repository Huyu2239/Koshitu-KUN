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

    @cog_ext.cog_slash(name='open', description='個室を開いた人以外も自由に閲覧、書き込みできる個室を開設します。')
    async def slash_say(self, ctx: SlashContext):
        if ctx.channel.id != self.bot.open_ch_id:
            return
        channel = await self.bot.category.create_text_channel(name=ctx.author.name)
        await channel.set_permissions(ctx.author, manage_channels=True)

        msg = await channel.send(f'<@{ctx.author.id}>\n個室を作成しました。')
        embed = discord.Embed(description=f'{channel.mention}')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Open(bot))
