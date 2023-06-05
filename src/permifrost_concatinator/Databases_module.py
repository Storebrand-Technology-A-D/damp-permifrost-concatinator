from .Base_module import Base_Module
import logging


class Databases_Module(Base_Module):
    def __init__(self):
        self.spesification = {}
        self.type = "Database"
        self.log = logging.getLogger(__name__)

    def __get_users(self):
        users = []
        self.log.info(f"Getting users from {self.type}s")
        for database in self.spesification:
            self.log.debug(f"Getting users from {self.type}: {database}")
            if "owner" in self.spesification[database]:
                self.log.debug(f"Adding owner: {self.spesification[database]['owner']}")
                users.append(self.spesification[database]["owner"])
                self.log.debug(f"Current users: {users}")
        return list(set(users))
