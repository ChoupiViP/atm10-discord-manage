import discord
from discord import app_commands
from discord.ext import commands
from docker.errors import DockerException

from bot.config_manager import ConfigManager
from bot.logger import logger
from bot.services.docker_service import DockerService
from bot.utils.permissions import Permissions


class SetupView(discord.ui.View):
    """Vue pour sélectionner un container Docker"""
    
    def __init__(self, containers: list):
        super().__init__()
        self.selected_container = None
        
        # Limiter à 25 options (limite Discord)
        containers = containers[:25]
        
        # Créer les options pour le select
        options = [
            discord.SelectOption(
                label=container["name"],
                value=container["id"],
                description=f"Status: {container['status']}"
            )
            for container in containers
        ]
        
        # Ajouter le select au view
        self.select.options = options
    
    @discord.ui.select(
        placeholder="Sélectionnez un container Docker",
        min_values=1,
        max_values=1
    )
    async def select(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.selected_container = select.values[0]
        self.stop()
        
        # Trouver le nom du container depuis son ID
        container_name = None
        for option in select.options:
            if option.value == self.selected_container:
                container_name = option.label
                break
        
        # Sauvegarder la configuration
        ConfigManager.set_docker_container(container_name)
        
        embed = discord.Embed(
            title="✅ Container configuré",
            description=f"Le container **{container_name}** a été défini par défaut.",
            color=discord.Color.green()
        )
        
        await interaction.response.edit_message(embed=embed, view=None)


class Setup(commands.Cog):
    """Cog pour la configuration du bot"""
    
    def __init__(self, bot):
        self.bot = bot
        self.docker = DockerService()
    
    @app_commands.command(
        name="setup",
        description="Configure le container Docker par défaut"
    )
    @app_commands.describe(
        container="Nom du container Docker à utiliser (optionnel - affiche une liste sinon)"
    )
    async def setup(
        self,
        interaction: discord.Interaction,
        container: str = None
    ):
        """Configure le container Docker utilisé par le bot"""
        
        # Vérifier les permissions
        if not Permissions.has_permission(interaction):
            embed = discord.Embed(
                title="❌ Accès refusé",
                description="Vous n'avez pas la permission d'utiliser cette commande.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        try:
            # Récupérer la liste des containers
            self.docker.connect()
            containers = self.docker.client.containers.list(all=True)
            
            if not containers:
                embed = discord.Embed(
                    title="❌ Erreur",
                    description="Aucun container Docker trouvé.",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            # Si un container est spécifié, le valider et le définir directement
            if container:
                for c in containers:
                    if c.name == container:
                        ConfigManager.set_docker_container(container)
                        embed = discord.Embed(
                            title="✅ Container configuré",
                            description=f"Le container **{container}** a été défini par défaut.",
                            color=discord.Color.green()
                        )
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                        logger.info(f"{interaction.user} a configuré le container: {container}")
                        return
                
                embed = discord.Embed(
                    title="❌ Container non trouvé",
                    description=f"Le container **{container}** n'existe pas.",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            # Préparer les données des containers
            container_data = [
                {
                    "name": c.name,
                    "id": c.id[:12],
                    "status": c.status
                }
                for c in containers
            ]
            
            # Créer et afficher la vue de sélection
            view = SetupView(container_data)
            
            embed = discord.Embed(
                title="🔧 Configuration du container Docker",
                description="Sélectionnez le container Docker à utiliser par défaut.",
                color=discord.Color.blue()
            )
            
            # Ajouter les containers à l'embed pour la visibilité
            for i, c in enumerate(container_data[:10], 1):
                embed.add_field(
                    name=f"{i}. {c['name']}",
                    value=f"Status: `{c['status']}`",
                    inline=False
                )
            
            if len(container_data) > 10:
                embed.add_field(
                    name=f"... et {len(container_data) - 10} autre(s)",
                    value="Consultez le menu déroulant ci-dessous.",
                    inline=False
                )
            
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
            logger.info(f"{interaction.user} a accédé au setup")
        
        except DockerException as e:
            logger.error(f"Erreur Docker: {e}")
            embed = discord.Embed(
                title="❌ Erreur Docker",
                description=f"Impossible de communiquer avec Docker.\n\n```{str(e)}```",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        except Exception as e:
            logger.exception(f"Erreur lors du setup: {e}")
            embed = discord.Embed(
                title="❌ Erreur",
                description=f"Une erreur est survenue.\n\n```{str(e)}```",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Setup(bot))
