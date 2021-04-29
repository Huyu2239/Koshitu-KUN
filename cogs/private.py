import asyncio
import discord
from discord.ext import commands
from discord_slash import SlashContext, cog_ext


class Private(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.slash_say.allowed_guild_ids = [bot.guild_id]
        asyncio.create_task(self.bot.slash.sync_all_commands())

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    @cog_ext.cog_slash(name='private', description='管理人・副管理人・権限で許可した人にしか見えなくなる部屋を開設します。')
    async def slash_say(self, ctx: SlashContext):
        if ctx.channel.id != self.bot.com_ch_id:
            return
        channel = await self.bot.category.create_text_channel(name=ctx.author.name)
        await channel.set_permissions(ctx.guild.get_role(self.bot.member_id), read_messages=False)
        await channel.set_permissions(ctx.author, read_messages=True)

        msg = await channel.send(f'<@{ctx.author.id}>\nプライベートチャンネルを作成しました。')
        embed = discord.Embed(description=f'{channel.mention}')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Private(bot))
