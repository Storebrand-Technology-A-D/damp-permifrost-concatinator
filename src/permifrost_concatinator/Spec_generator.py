import logging
from .txt_generator import txt_generator


class Permifrost_Spec_Generator:
    def __init__(self, version):
        self.version = version
        self.output = ""
        self.users = ""
        self.databases = ""
        self.warehouses = ""
        self.functional_roles = ""
        self.access_roles = ""
        self.roles = ""
        self.space = " " * 2
        self.log = logging.getLogger(__name__)
        self.log.info("Spec generator initialized")
        self.txt = txt_generator(2)

    def generate_users(self, module):
        self.log.info("Generating users")
        self.users = "users:\n"
        for user in module.spesification:
            self.log.info(f"Generating user: {user}")
            self.log.debug(f"User spec: {module.spesification[user]}")
            result = self.txt.generate_users(user, module.spesification[user])
            self.log.debug(f"user output:\n{result}")
            self.users += result

    def generate_databases(self, module):
        self.log.info("Generating databases")
        self.databases = "databases:\n"
        for database in module.spesification:
            result = self.txt.generate_databases(
                database, module.spesification[database]
            )
            self.log.debug(f"database output:\n{result}")
            self.databases += result

    def generate_warehouses(self, module):
        self.log.info("Generating warehouses")
        self.warehouses = "warehouses:\n"
        for warehouse in module.spesification:
            result = self.txt.generate_warehouses(
                warehouse, module.spesification[warehouse]
            )
            self.log.debug(f"warehouse output:\n{result}")
            self.warehouses += result

    def generate_roles(self, module):
        self.log.info("Generating roles")
        self.roles = "roles:\n"
        try:
            self.__functional_role(module)
            self.__access_role(module)
            self.log.info(f"Functional and Accsess roles have been generated")
        except:
            self.log.info(f"spec contained either accsess or functional roles only")
            if module.functional_roles != []:
                self.__functional_role(module)
            elif module.access_roles != []:
                self.__access_role(module)
            else:
                self.log.error("No roles found in module")
                raise Exception("No roles found in module")
            self.log.info(f"Roles have been generated")

        self.log.debug(f"Functional roles output:\n{self.functional_roles}")
        self.log.debug(f"Access roles output:\n{self.access_roles}")
        self.roles += f"{self.functional_roles}"
        self.roles += f"{self.access_roles}"
        self.log.debug(f"Roles output:\n{self.roles}")

    def __access_role(self, module):
        self.log.info("Generating access roles")
        for access_role in module.access_roles:
            self.log.info(f"Generating access role: {access_role}")
            self.log.debug(f"Access role spec: {module.spesification[access_role]}")
            result = self.txt.generate_accsess_role(
                access_role, module.spesification[access_role]
            )
            self.log.debug(f"Access role output:\n{result}")
            self.access_roles += result
        self.log.info("Accses role generation complete")

    def __functional_role(self, module):
        self.log.info("Generating functional roles")
        for functional_role in module.functional_roles:
            self.log.info(f"Generating functional role: {functional_role}")
            self.log.debug(
                f"Functional role spec: {module.spesification[functional_role]}"
            )
            result = self.txt.generate_functional_role(
                functional_role, module.spesification[functional_role]
            )
            self.log.debug(f"Functional role output:\n{result}")
            self.functional_roles += result
        self.log.info("Functional role generation complete")
        self.functional_roles += "\n"

    def generate(self, module):
        if module.type == "User":
            self.generate_users(module)
        elif module.type == "Database":
            self.generate_databases(module)
        elif module.type == "Warehouse":
            self.generate_warehouses(module)
        elif module.type == "Role":
            self.generate_roles(module)

    def get_output(self):
        self.output += f"""version: \"{self.version}\"\n"""
        self.output += self.databases
        self.output += self.roles
        self.output += self.users
        self.output += self.warehouses

        return self.output
