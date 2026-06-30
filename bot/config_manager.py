import json
from pathlib import Path
from bot.logger import logger

class ConfigManager:
    """Gestionnaire de configuration persistante"""
    
    CONFIG_FILE = Path(__file__).parent.parent / "data" / "config.json"
    
    @classmethod
    def _ensure_data_dir(cls):
        """Crée le dossier data s'il n'existe pas"""
        cls.CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def _load_config(cls) -> dict:
        """Charge la configuration depuis le fichier JSON"""
        cls._ensure_data_dir()
        
        if cls.CONFIG_FILE.exists():
            try:
                with open(cls.CONFIG_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Erreur lors de la lecture de la config: {e}")
                return {}
        return {}
    
    @classmethod
    def _save_config(cls, config: dict):
        """Sauvegarde la configuration dans le fichier JSON"""
        cls._ensure_data_dir()
        
        try:
            with open(cls.CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde de la config: {e}")
    
    @classmethod
    def get_docker_container(cls) -> str:
        """Récupère le container Docker configuré"""
        config = cls._load_config()
        return config.get("docker_container")
    
    @classmethod
    def set_docker_container(cls, container_name: str):
        """Définit le container Docker configuré"""
        config = cls._load_config()
        config["docker_container"] = container_name
        cls._save_config(config)
        logger.info(f"Container Docker défini à: {container_name}")
    
    @classmethod
    def get_guild_config(cls, guild_id: int) -> dict:
        """Récupère la configuration spécifique d'une guilde"""
        config = cls._load_config()
        guilds = config.get("guilds", {})
        return guilds.get(str(guild_id), {})
    
    @classmethod
    def set_guild_config(cls, guild_id: int, guild_config: dict):
        """Définit la configuration spécifique d'une guilde"""
        config = cls._load_config()
        if "guilds" not in config:
            config["guilds"] = {}
        config["guilds"][str(guild_id)] = guild_config
        cls._save_config(config)
        logger.info(f"Configuration de la guilde {guild_id} mise à jour")
