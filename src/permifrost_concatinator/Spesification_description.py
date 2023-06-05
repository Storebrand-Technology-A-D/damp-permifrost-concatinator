class Spessification_description:
    def __init__(self):
        self.count_modules = 0
        self.entities = []

    def load_module_description(self, module_name, module_description):
        if module_name == "databases":
            self.databases = module_description.return_description()
        elif module_name == "warehouses":
            self.warehouses = module_description.return_description()
        elif module_name == "users":
            self.users = module_description.return_description()
        elif module_name == "roles":
            self.roles = module_description.return_description()
        else:
            raise Exception("Module not found")
