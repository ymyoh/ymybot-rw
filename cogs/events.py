# -*- coding: utf-8 -*-

import discord
import datetime
from utils import config
from discord.ext import commands


def setup(bot):
    bot.add_cog(Events(bot))


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _change_presence(self):
        guild = self.bot.get_guild(config.DEFAULT_GUILD_ID)
        bots = sum(m.bot for m in guild.members)
        humans = guild.member_count - bots

        await self.bot.change_presence(
            activity=discord.Activity(
                type=config.ACTIVITY_TYPE, name=f"{humans:,d} + {bots} üyeyi",
            ),
            status=config.STATUS_TYPE,
        )

    @commands.Cog.listener()
    async def on_ready(self):
        if not hasattr(self, "uptime"):
            self.bot.uptime = datetime.datetime.now()

        print(
            f"{self.bot.user} (ID: {self.bot.user.id})\n"
            f"discord.py version: {discord.__version__}"
        )

        await self._change_presence()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self._change_presence()

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await self._change_presence()

    @commands.Cog.listener(name="on_message")
    async def on_bot_mention(self, message):
        author = message.author

        if (
            self.bot.user.mentioned_in(message)
            and message.mention_everyone is False
        ):
            channel = self.bot.get_channel(config.MENTION_LOG_CHANNEL_ID)

            embed = discord.Embed(color=self.bot.color)
            embed.description = message.content
            embed.set_author(name=author, icon_url=author.avatar_url)
            embed.set_footer(text=f"ID: {author.id}")
            embed.add_field(
                name="Bahsetme Bilgisi",
                value=f"Mesaja [zıpla!]({message.jump_url})\n"
                f"{author.guild} ({author.guild.id})",
            )
            if message.attachments:
                attachment_url = message.attachments[0].url
                embed.set_image(url=attachment_url)
            await channel.send(embed=embed)

    @commands.Cog.listener(name="on_message")
    async def on_dm_message(self, message):
        author = message.author

        if message.guild is None:
            channel = self.bot.get_channel(config.DM_LOG_CHANNEL_ID)

            embed = discord.Embed(color=self.bot.color)
            embed.description = message.content
            embed.set_author(name=author, icon_url=author.avatar_url)
            embed.set_footer(text=f"ID: {author.id}")
            if message.attachments:
                attachment_url = message.attachments[0].url
                embed.set_image(url=attachment_url)
            await channel.send(embed=embed)
