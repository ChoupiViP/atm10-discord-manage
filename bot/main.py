import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

# Vérification du token
if TOKEN is None:
    raise ValueError("Le token Discord est introuvable dans le fichier .env")

# Intents
intents = discord.Intents.default()

# Création du bot
bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# Événement au démarrage
@bot.event
async def on_ready():
    print("=" * 40)
    print(f"Connecté en tant que : {bot.user}")
    print(f"ID : {bot.user.id}")

    try:
        synced = await bot.tree.sync()
        print(f"Commandes synchronisées : {len(synced)}")
    except Exception as e:
        print(e)

    print("=" * 40)

# Commande /ping
@bot.tree.command(
    name="ping",
    description="Vérifie si le bot est en ligne."
)
async def ping(interaction: discord.Interaction):

    latency = round(bot.latency * 1000)

    await interaction.response.send_message(
        f"🏓 Pong ! `{latency} ms`"
    )

# Lancement du bot
bot.run(TOKEN)