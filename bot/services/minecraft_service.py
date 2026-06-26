from bot.services.docker_service import DockerService


class MinecraftService:
    def __init__(self):
        self.docker = DockerService()

    def get_status(self):
        return self.docker.get_status()

    # À venir
    def start(self):
        pass

    def stop(self):
        pass

    def restart(self):
        pass