import asyncio

from discord.ext import commands
from discord_slash import SlashContext, cog_ext


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        asyncio.create_task(self.bot.slash.sync_all_commands())

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    @cog_ext.cog_slash(name='open', description='部屋を開いた人以外も自由に閲覧、書き込みできる部屋を開設します。', guild_ids=[self.bot.guild_id])
    async def slash_say(self, ctx: SlashContext):
        channel = await self.bot.category.create_text_channel(name=ctx.author.name)
        await channel.send(f'<@{ctx.author.id}>\nオープンチャンネルを作成しました。')

def setup(bot):
    bot.add_cog(Ping(bot))
