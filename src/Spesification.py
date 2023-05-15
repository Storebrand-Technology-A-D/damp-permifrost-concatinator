from src.Databases import Databases_Module
from src.Warehouses import Warehouses_Module
from src.Users import Users_Module
from src.Roles import Roles_Module


class Spesification:
    """
    Class for holding onto a permifrost spessification as imported from a spec file.

    """

    def __init__(self):
        self.databases = Databases_Module()
        self.warehouses = Warehouses_Module()
        self.users = Users_Module()
        self.roles = Roles_Module()
        self.spec_file = {}

    def load(self, spec_file):
        self.spec_file = spec_file

    def identify_modules(self):
        """
        Identify the modules in the spec file.
        """
        self.module_list = list(self.spec_file.keys())
        self.module_list.remove("version")

    def identify_entities(self):
        """
        Identify the entities in the spec file.
        """
        for module in self.module_list:
            if module == "roles":
                self.roles.add_entities(self.spec_file[module])
            elif module == "users":
                self.users.add_entities(self.spec_file[module])
            elif module == "warehouses":
                self.warehouses.add_entities(self.spec_file[module])
            elif module == "databases":
                self.databases.add_entities(self.spec_file[module])
            else:
                raise Exception("Module not found")
        return True
