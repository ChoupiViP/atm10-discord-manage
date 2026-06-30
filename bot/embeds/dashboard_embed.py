from datetime import datetime

import discord


class DashboardEmbed:

    @staticmethod
    def create(info: dict):

        status = "🟢 En ligne" if info["status"] == "running" else "🔴 Hors ligne"

        embed = discord.Embed(
            title="🎮 ATM10 TO THE SKY",
            description="Dashboard du serveur Minecraft",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="🖥 Serveur",
            value=status,
            inline=False
        )

        embed.add_field(
            name="🐳 Docker",
            value=info["status"],
            inline=True
        )

        embed.add_field(
            name="📦 Conteneur",
            value=info["name"],
            inline=True
        )

        embed.add_field(
            name="👥 Joueurs",
            value="Bientôt...",
            inline=True
        )

        embed.add_field(
            name="🧠 RAM",
            value="Bientôt...",
            inline=True
        )

        embed.add_field(
            name="⚡ CPU",
            value="Bientôt...",
            inline=True
        )

        embed.set_footer(
            text=f"Dernière mise à jour : {datetime.now().strftime('%H:%M:%S')}"
        )

        return embed