import discord
from discord.ext import commands
from discord_slash import SlashCommand
from dotenv import load_dotenv
import os

load_dotenv()


class Mybot(commands.Bot):
    def __init__(self, command_prefix, **options):
        self.command_prefix = command_prefix
        prefix = commands.when_mentioned_or(command_prefix)
        allowed_mentions = discord.AllowedMentions(everyone=False, roles=False, users=True)
        intents = discord.Intents.all()
        super().__init__(
            command_prefix=prefix,
            intents=intents,
            allowed_mentions=allowed_mentions,
            **options
        )
        self.slash_client = SlashCommand(self, sync_commands=True)
        self.owner_id = int(os.environ['OWNER_ID'])
        self.guild_id = int(os.environ['GUILD_ID'])
        self.log_ch_id = int(os.environ['LOG_CH_ID'])
        self.com_ch_id = 836963480069865492
        self.member_id = 837168066516746260


    async def on_ready(self):
        self.category = await self.fetch_channel(int(os.environ['CATEGORY_ID']))
        for cog in os.listdir("./cogs"):
            if cog.endswith(".py"):
                try:
                    self.load_extension(f"cogs.{cog[:-3]}")
                except commands.ExtensionAlreadyLoaded:
                    self.reload_extension(f"cogs.{cog[:-3]}")
                except discord.ext.commands.errors.ExtensionFailed:
                    continue
        print('ready')
        await self.change_presence(activity=discord.Game(name=f"/help"))

    async def on_guild_join(self, guild):
        if guild.id !=self.guild_id:
            await guild.leave()


if __name__ == '__main__':
    bot = Mybot(command_prefix="k.")
    bot.run(os.environ['TOKEN'])
