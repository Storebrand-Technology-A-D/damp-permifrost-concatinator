class Spec_Generator:
    def __init__(self, version):
        self.version = version
        self.output = ""
        self.users = "\n"
        self.databases = "\n"
        self.warehouses = "\n"
        self.functional_roles = ""
        self.access_roles = ""
        self.roles = "\n"

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
                    self.users += (
                        f"""      {key}: {module.spesification[user][key]}\n"""
                    )

    def generate_databases(self, module):
        self.databases = "databases:\n"
        for database in module.spesification:
            self.databases += f"""  - {database}:\n"""
            for key in module.spesification[database]:
                if key == "owner":
                    self.databases += (
                        f"""      {key}: {module.spesification[database][key]}\n"""
                    )
                elif key == "shared":
                    self.databases += (
                        f"""      {key}: {module.spesification[database][key]}\n"""
                    )

    def generate_warehouses(self, module):
        self.warehouses = "warehouses:\n"
        for warehouse in module.spesification:
            self.warehouses += f"""  - {warehouse}:\n"""
            for key in module.spesification[warehouse]:
                self.warehouses += (
                    f"""      {key}: {module.spesification[warehouse][key]}\n"""
                )

    def generate_roles(self, module):
        self.roles = "roles:\n"
        try:
            self.__functional_role(module)
            self.__access_role(module)
        except:
            if module.functional_roles != []:
                self.__functional_role(module)
            elif module.access_roles != []:
                self.__access_role(module)
            else:
                raise Exception("No roles found in module")
        
        self.roles += f"{self.functional_roles}"
        self.roles += f"{self.access_roles}"

    def __access_role(self, module):
        for access_role in module.access_roles:
            self.access_roles += f"""  - {access_role}:\n"""
            for key in module.spesification[access_role]:
                if key == "privileges":
                    self.access_roles += f"""    {key}:\n"""
                    for privilege in module.spesification[access_role][key]:
                        self.access_roles += f"""      {privilege}:\n"""
                        for read_write in module.spesification[access_role][key][
                            privilege
                        ]:
                            self.access_roles += f"""        {read_write}:\n"""
                            for database in module.spesification[access_role][key][
                                privilege
                            ][read_write]:
                                self.access_roles += (
                                    f"""          - {database}\n"""
                                )

    def __functional_role(self, module):
        for functional_role in module.functional_roles:
            self.functional_roles += f"""  - {functional_role}:\n"""
            for key in module.spesification[functional_role]:
                if key == "member_of":
                    self.functional_roles += f"""    {key}:\n"""
                    for role in module.spesification[functional_role][key]:
                        self.functional_roles += f"""      - {role}\n"""
                elif key == "warehouses":
                    self.functional_roles += f"""    {key}:\n"""
                    for warehouse in module.spesification[functional_role][key]:
                        self.functional_roles += f"""      - {warehouse}\n"""
        self.functional_roles += "\n"

    def generate(self, module):
        self.output += f"""version: \"{self.version}\"\n"""
        if module.type == "User":
            self.generate_users(module)
        elif module.type == "Database":
            self.generate_databases(module)
        elif module.type == "Warehouse":
            self.generate_warehouses(module)
        elif module.type == "Role":
            self.generate_roles(module)

        self.output += self.users
