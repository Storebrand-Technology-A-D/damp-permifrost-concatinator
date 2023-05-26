from src.Databases_module import Databases_Module
from src.Warehouses_module import Warehouses_Module
from src.Users_module import Users_Module
from src.Roles_module import Roles_Module
from src.Spesification_description import Spessification_description
from src.Reader import Reader
from src.Spec_generator import Spec_Generator
from src.Writer_yaml_file import Yaml_file_Writer


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
        reader = Reader()
        try:
            self.spec_file = reader.get_file(spec_file)
            self.identify_modules()
        except:
            reader.read_dir(spec_file)
            if len(reader.files) == 0:
                raise Exception("No files found")
            elif len(reader.files) == 1:
                self.spec_file = reader.get_file(reader.files[0])
                self.identify_modules()
            else:
                self.spec_file = reader.get_file(reader.files[0])
                self.identify_modules()
                self.identify_entities()
                for file in reader.files[1:]:
                    self.append_spec(reader.get_file(file))

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
                self.roles.identify_roles()
            elif module == "users":
                self.users.add_entities(self.spec_file[module])
            elif module == "warehouses":
                self.warehouses.add_entities(self.spec_file[module])
            elif module == "databases":
                self.databases.add_entities(self.spec_file[module])
            else:
                raise Exception("Module not found")
        return True

    def append_spec(self, spec_file):
        """
        Append a spec file to the current spec.
        """
        new_spec_file = spec_file
        new_module_list = list(new_spec_file.keys())
        new_module_list.remove("version")
        for module in new_module_list:
            if module == "roles":
                self.roles.add_entities(new_spec_file[module])
                self.roles.identify_roles()
            elif module == "users":
                self.users.add_entities(new_spec_file[module])
            elif module == "warehouses":
                self.warehouses.add_entities(new_spec_file[module])
            elif module == "databases":
                self.databases.add_entities(new_spec_file[module])
            else:
                raise Exception("Module not found")

    def describe(self):
        """
        Provides a general description of the spesification.
        That can be used to validate the spesification.
        """
        description = Spessification_description()
        for module in self.module_list:
            if module == "roles":
                description.load_module_description("roles", self.roles.describe())
            elif module == "users":
                description.load_module_description("users", self.users.describe())
            elif module == "warehouses":
                description.load_module_description(
                    "warehouses", self.warehouses.describe()
                )
            elif module == "databases":
                description.load_module_description(
                    "databases", self.databases.describe()
                )
            else:
                raise Exception("Module not found")
        return description

    def generate(self):
        self.output = ""
        generator = Spec_Generator("0.14.0")
        generator.generate(self.roles)
        generator.generate(self.users)
        generator.generate(self.warehouses)
        generator.generate(self.databases)

        self.output = generator.get_output()
        self.generated = True
        return self.output

    def export(self, file_name, writer=Yaml_file_Writer()):
        if self.generated:
            writer.write(file_name, self.output)
            self.exported = True
        else:
            raise Exception("Spec not generated")
