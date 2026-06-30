from bot.services.docker_service import DockerService


class MinecraftService:

    def __init__(self):
        self.docker = DockerService()

    def get_status(self):
        return self.docker.get_status()

    def start(self):
        self.docker.start_container()

    def stop(self):
        self.docker.stop_container()

    def restart(self):
        self.docker.restart_container()