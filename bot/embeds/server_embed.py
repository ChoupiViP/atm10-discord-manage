import discord


class ServerEmbed:

    @staticmethod
    def status(info: dict) -> discord.Embed:

        color = (
            discord.Color.green()
            if info["status"] == "running"
            else discord.Color.red()
        )

        embed = discord.Embed(
            title="🎮 ATM10 To The Sky",
            description="Informations du serveur Minecraft",
            color=color
        )

        embed.add_field(
            name="📦 Conteneur",
            value=info["name"],
            inline=True
        )

        embed.add_field(
            name="📊 Statut",
            value=info["status"].capitalize(),
            inline=True
        )

        embed.add_field(
            name="👥 Joueurs",
            value=f"{info.get('players', 'N/A')} / {info.get('max_players', 'N/A')}",
            inline=True
        )

        embed.add_field(
            name="⏱️ TPS",
            value=info.get("tps", "N/A"),
            inline=True
        )

        embed.add_field(
            name="🏷️ Image",
            value=info["image"],
            inline=False
        )

        embed.add_field(
            name="🔄 Redémarrage",
            value=info["restart"],
            inline=False
        )

        embed.set_footer(text="ATM10 Discord Manager • v0.5.0")

        return embed

    @staticmethod
    def success(message: str):

        embed = discord.Embed(
            title="✅ Succès",
            description=message,
            color=discord.Color.green()
        )

        return embed

    @staticmethod
    def error(message: str):

        embed = discord.Embed(
            title="❌ Erreur",
            description=message,
            color=discord.Color.red()
        )

        return embed