import asyncio

from discord.ext import commands
from discord_slash import SlashContext, cog_ext


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.category = self.bot.get_guild(self.bot.guild_id).get_channel(self.bot.category_id)
        asyncio.create_task(self.bot.slash.sync_all_commands())

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    @cog_ext.cog_slash(name='private', description='管理人・副管理人・権限で許可した人にしか見えなくなる部屋を開設します。', guild_ids=[self.bot.guild_id])
    async def slash_say(self, ctx: SlashContext):
        channel = await self.bot.category.create_text_channel(name=ctx.author.name)
        await channel.send(f'<@{ctx.author.id}>\nプライベートチャンネルを作成しました。')



def setup(bot):
    bot.add_cog(Ping(bot))
