import discord
from discord import app_commands
from discord.ext import commands


class Status(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="status",
        description="Affiche l'état du bot."
    )
    async def status(self, interaction: discord.Interaction):

        embed = discord.Embed(
            title="ATM10 Discord Manager",
            description="Le bot fonctionne correctement.",
            color=discord.Color.green()
        )

        embed.add_field(
            name="Version",
            value="v0.2",
            inline=True
        )

        embed.add_field(
            name="Latence",
            value=f"{round(self.bot.latency * 1000)} ms",
            inline=True
        )

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Status(bot))