class Databases_Module:
    def __init__(self):
        self.spesification = {}

    def add_entities(self, databases):
        for database in databases:
            self.spesification.update(database)

    def get_entitiy(self, database):
        if database not in self.spesification:
            raise Exception("Database not found")
        return self.spesification[database]

    def is_entity(self, database):
        return database in self.spesification

    def __get_users(self):
        users = []
        for database in self.spesification:
            if "owner" in self.spesification[database]:
                users.append(self.spesification[database]["owner"])
        return list(set(users))

    def describe(self):
        self.count = len(self.spesification)
        self.entities = list(self.spesification.keys())
        self.users = self.__get_users()
        return self
