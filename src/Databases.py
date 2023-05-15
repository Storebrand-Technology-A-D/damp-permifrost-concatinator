from src.Base_module import Base_Module

class Databases_Module(Base_Module):
    def __init__(self):
        self.spesification = {}
        self.type = "Database"

    def __get_users(self):
        users = []
        for database in self.spesification:
            if "owner" in self.spesification[database]:
                users.append(self.spesification[database]["owner"])
        return list(set(users))
