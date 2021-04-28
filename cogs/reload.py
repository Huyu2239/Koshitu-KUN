import json
import os

from discord.ext import commands


class Reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.author.id == self.bot.owner_id

    @commands.command(hidden=True)
    async def reload(self, ctx, path=None):
        msg = await ctx.send('更新中')
        for cog in os.listdir('./cogs/*.py'):
            if cog == 'reload.py':
                continue
            try:
                self.bot.reload_extension(f'cogs.{cog[:-3]}')
            except commands.ExtensionNotLoaded:
                self.bot.load_extension(f'cogs.{cog[:-3]}')
        await msg.edit(content='更新しました')
        print('--------------------------------------------------')


def setup(bot):
    bot.add_cog(Reload(bot))
