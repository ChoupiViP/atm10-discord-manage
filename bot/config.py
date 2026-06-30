import os
from dotenv import load_dotenv
from bot.config_manager import ConfigManager

load_dotenv()

class Config:
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    AUTHORIZED_ROLE = os.getenv("AUTHORIZED_ROLE", "Admin")
    
    # DOCKER_CONTAINER peut être défini via .env ou via la commande /setup
    @classmethod
    def get_docker_container(cls):
        """Récupère le container Docker (d'abord .env, puis config persistante)"""
        env_container = os.getenv("DOCKER_CONTAINER")
        if env_container:
            return env_container
        
        persisted_container = ConfigManager.get_docker_container()
        if persisted_container:
            return persisted_container
        
        raise ValueError("DOCKER_CONTAINER manquant - définissez-le via .env ou utilisez /setup")

    if not DISCORD_TOKEN:
        raise ValueError("DISCORD_TOKEN manquant")