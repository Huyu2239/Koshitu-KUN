import asyncio
import discord
from discord.ext import commands
from discord_slash import SlashContext, cog_ext


class Del(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.slash_say.allowed_guild_ids = [bot.guild_id]
        asyncio.create_task(self.bot.slash.sync_all_commands())

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    @cog_ext.cog_slash(name='del', description='チャンネルの削除')
    async def slash_say(self, ctx: SlashContext):
        msg = (await ctx.channel.history(limit=1, oldest_first=True).flatten())[0]
        if str(ctx.author.id) in msg.content:
            await ctx.channel.send('チャンネル削除中・・・')
            await asyncio.sleep(2)
            await ctx.channel.delete()
        else:
            embed = discord.Embed(title='ERROR', description='他の人が作成したチャンネルを削除することはできません。')
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Del(bot))
