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
        self.space = " "*2

    def generate_users(self, module):
        self.users = "users:\n"
        for user in module.spesification:
            self.users += f"""{self.space*1}- {user}:\n"""
            for key in module.spesification[user]:
                if key == "member_of":
                    self.users += f"""{self.space*2}{key}:\n"""
                    for role in module.spesification[user][key]:
                        self.users += f"""{self.space*3}- {role}\n"""
                elif key == "can_login":
                    self.users += (
                        f"""{self.space*2}{key}: {module.spesification[user][key]}\n"""
                    )

    def generate_databases(self, module):
        self.databases = "databases:\n"
        for database in module.spesification:
            self.databases += f"""{self.space*1}- {database}:\n"""
            for key in module.spesification[database]:
                if key == "owner":
                    self.databases += (
                        f"""{self.space*2}{key}: {module.spesification[database][key]}\n"""
                    )
                elif key == "shared":
                    self.databases += (
                        f"""{self.space*2}{key}: {module.spesification[database][key]}\n"""
                    )

    def generate_warehouses(self, module):
        self.warehouses = "warehouses:\n"
        for warehouse in module.spesification:
            self.warehouses += f"""{self.space*1}- {warehouse}:\n"""
            for key in module.spesification[warehouse]:
                self.warehouses += (
                    f"""{self.space*2}{key}: {module.spesification[warehouse][key]}\n"""
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
            self.access_roles += f"""{self.space*1}- {access_role}:\n"""
            for key in module.spesification[access_role]:
                if key == "privileges":
                    self.access_roles += f"""{self.space*2}{key}:\n"""
                    for privilege in module.spesification[access_role][key]:
                        self.access_roles += f"""{self.space*3}{privilege}:\n"""
                        for read_write in module.spesification[access_role][key][
                            privilege
                        ]:
                            self.access_roles += f"""{self.space*4}{read_write}:\n"""
                            for database in module.spesification[access_role][key][
                                privilege
                            ][read_write]:
                                self.access_roles += (
                                    f"""{self.space*5}- {database}\n"""
                                )

    def __functional_role(self, module):
        for functional_role in module.functional_roles:
            self.functional_roles += f"""{self.space*1}- {functional_role}:\n"""
            for key in module.spesification[functional_role]:
                if key == "member_of":
                    self.functional_roles += f"""{self.space*2}{key}:\n"""
                    for role in module.spesification[functional_role][key]:
                        self.functional_roles += f"""{self.space*3}- {role}\n"""
                elif key == "warehouses":
                    self.functional_roles += f"""{self.space*2}{key}:\n"""
                    for warehouse in module.spesification[functional_role][key]:
                        self.functional_roles += f"""{self.space*3}- {warehouse}\n"""
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

        self.output += self.databases
        self.output += self.roles
        self.output += self.users
        self.output += self.warehouses

        return self.output
