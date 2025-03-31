from dataclasses import dataclass
import discord

@dataclass
class DiscordContext:
    client: discord.Client
    guild_id: int

    def __init__(self, client: discord.Client, guild_id: int):
        self.client = client
        self.guild_id = guild_id
