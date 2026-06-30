import docker
from docker.errors import DockerException, NotFound

from bot.config import Config


class DockerService:
    def __init__(self):
        self.client = None

    def connect(self):
        if self.client is None:
            self.client = docker.from_env()

    def get_container(self):
        self.connect()
        container_name = Config.get_docker_container()
        return self.client.containers.get(container_name)

    def get_status(self):
        try:
            container = self.get_container()

            container.reload()

            return {
                "success": True,
                "name": container.name,
                "status": container.status,
                "image": container.image.tags[0] if container.image.tags else "Aucune",
                "restart": container.attrs["HostConfig"]["RestartPolicy"]["Name"],
            }

        except (DockerException, NotFound) as e:
            return {
                "success": False,
                "error": str(e)
            }

    def start_container(self):
        container = self.get_container()
        container.start()

    def stop_container(self):
        container = self.get_container()
        container.stop()

    def restart_container(self):
        container = self.get_container()
        container.restart()