import docker

from bot.config import Config


class DockerService:
    def __init__(self):
        self.client = None

    def connect(self):
        if self.client is None:
            self.client = docker.from_env()

    def get_container(self):
        self.connect()
        return self.client.containers.get(Config.DOCKER_CONTAINER)

    def get_status(self):
        container = self.get_container()

        return {
            "name": container.name,
            "status": container.status,
            "image": container.image.tags[0] if container.image.tags else "Aucune",
            "restart": container.attrs["HostConfig"]["RestartPolicy"]["Name"],
        }