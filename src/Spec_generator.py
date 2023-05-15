
class Spec_Generator():
    def __init__(self, version):
        self.version = version
        self.output = ""
        self.users = "\n"
        self.databases = "\n"
        self.warehouses = "\n"
        self.functional_roles = "\n"
        self.access_roles = "\n"

    def generate_users(self, module):
        self.users = "users:\n"
        for user in module.spesification:
            self.users += f"""  - {user}:\n"""
            for key in module.spesification[user]:
                if key == "member_of":
                    self.users += f"""      {key}:\n"""
                    for role in module.spesification[user][key]:
                        self.users += f"""        - {role}\n"""
                elif key == "can_login":
                    self.users += f"""      {key}: {module.spesification[user][key]}\n"""

    def generate_databases(self, module):
        self.databases = "databases:\n"
        for database in module.spesification:
            self.databases += f"""  - {database}:\n"""
            for key in module.spesification[database]:
                if key == "owner":
                    self.databases += f"""      {key}: {module.spesification[database][key]}\n"""
                elif key == "shared":
                    self.databases += f"""      {key}: {module.spesification[database][key]}\n"""

    def generate_warehouses(self, module):
        self.warehouses = "warehouses:\n"
        for warehouse in module.spesification:
            self.warehouses += f"""  - {warehouse}:\n"""
            for key in module.spesification[warehouse]:
                self.warehouses += f"""      {key}: {module.spesification[warehouse][key]}\n"""

    def generate(self, module):
        self.output += f"""version: \"{self.version}\"\n"""
        if module.type == "User":
            self.generate_users(module)
        elif module.type == "Database":
            self.generate_databases(module)
        elif module.type == "Warehouse":
            self.generate_warehouses(module)

        self.output += self.users