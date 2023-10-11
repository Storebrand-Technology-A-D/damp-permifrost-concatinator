from .Databases_module import Databases_Module
from .Warehouses_module import Warehouses_Module
from .Users_module import Users_Module
from .Roles_module import Roles_Module
from .Spesification_description import Spessification_description
from .Reader import Reader
from .Spec_generator import Permifrost_Spec_Generator
from .Writer_yaml_file import Yaml_file_Writer
from .verification_module import SpecVerification
import logging


class Spesification:
    """
    Class for holding onto a permifrost spessification as imported from a spec file.

    """

    def __init__(self, verification=False, generate_roles=False):
        self.databases = Databases_Module()
        self.warehouses = Warehouses_Module()
        self.users = Users_Module()
        self.roles = Roles_Module()
        self.spec_file = {}
        self.verification = verification
        self.roles_generation = generate_roles
        self.log = logging.getLogger(__name__)
        self.log.info("Spesification object created")

    def load(self, spec_file):
        self.log.info("Loading spec file: " + spec_file)
        reader = Reader()
        try:
            self.spec_file = reader.get_file(spec_file)
            self.identify_modules()
            self.log.info("Single file spec loaded")
        except:
            reader.read_dir(spec_file)
            if len(reader.files) == 0:
                self.log.error("No files found")
                raise Exception("No files found")
            elif len(reader.files) == 1:
                self.spec_file = reader.get_file(reader.files[0])
                self.identify_modules()
                self.log.info("Single file spec loaded")
            else:
                self.log.debug("Multiple files found")
                self.spec_file = reader.get_file(reader.files[0])
                self.log.debug("First file loaded: " + reader.files[0])
                self.identify_modules()
                self.identify_entities()
                for file in reader.files[1:]:
                    self.log.debug("Appending file: " + file)
                    self.append_spec(reader.get_file(file))
                self.log.info("Multiple file spec loaded")

    def identify_modules(self):
        """
        Identify the modules in the spec file.
        """
        self.module_list = list(self.spec_file.keys())
        self.module_list.remove("version")
        for module in self.module_list:
            self.spec_file[module] = sorted(
                self.spec_file[module], key=lambda d: list(d.keys())
            )
        self.log.debug("Modules identified: " + str(self.module_list))
        self.log.info("Modules identified")

    def identify_entities(self):
        """
        Identify the entities in the spec file.
        """
        self.log.debug("Identifying entities")
        self.log.debug("Using modules: " + str(self.module_list))
        for module in self.module_list:
            if module == "roles":
                self.log.info("Identifying roles")
                self.log.debug("Identifying roles: " + str(self.spec_file[module]))
                self.roles.add_entities(self.spec_file[module])
                self.roles.identify_roles()
                self.log.info("Roles identifcation complete")
            elif module == "users":
                self.log.info("Identifying users")
                self.log.debug("Identifying users: " + str(self.spec_file[module]))
                self.users.add_entities(self.spec_file[module])
                self.log.info("Users identifications complete")
            elif module == "warehouses":
                self.log.info("Identifying warehouses")
                self.log.debug("Identifying warehouses: " + str(self.spec_file[module]))
                self.warehouses.add_entities(self.spec_file[module])
                self.log.info("Warehouses identifications complete")
            elif module == "databases":
                self.log.info("Identifying databases")
                self.log.debug("Identifying databases: " + str(self.spec_file[module]))
                self.databases.add_entities(self.spec_file[module])
                self.log.info("Databases identifications complete")
            else:
                self.log.error("Module not found")
                raise Exception("Module not found")
        self.log.info("Entities identifications complete")
        return True

    def append_spec(self, spec_file):
        """
        Append a spec file to the current spec.
        """
        self.log.debug("Appending spec file: " + str(spec_file))
        new_spec_file = spec_file
        new_module_list = list(new_spec_file.keys())
        new_module_list.remove("version")
        for module in new_module_list:
            if module == "roles":
                self.log.debug("Appending roles: " + str(new_spec_file[module]))
                self.roles.add_entities(new_spec_file[module])
                self.roles.identify_roles()
                self.log.debug("Roles list: " + str(self.roles.spesification))
                self.log.info("Roles appended")
            elif module == "users":
                self.log.debug("Appending users: " + str(new_spec_file[module]))
                self.users.add_entities(new_spec_file[module])
                self.log.debug("Users list: " + str(self.users.spesification))
                self.log.info("Users appended")
            elif module == "warehouses":
                self.log.debug("Appending warehouses: " + str(new_spec_file[module]))
                self.warehouses.add_entities(new_spec_file[module])
                self.log.debug("Warehouses list: " + str(self.warehouses.spesification))
                self.log.info("Warehouses appended")
            elif module == "databases":
                self.log.debug("Appending databases: " + str(new_spec_file[module]))
                self.databases.add_entities(new_spec_file[module])
                self.log.debug("Databases list: " + str(self.databases.spesification))
                self.log.info("Databases appended")
            else:
                self.log.error("Module not found")
                raise Exception("Module not found")
        for module in self.module_list:
            for entity in new_spec_file[module]:
                if entity not in self.spec_file[module]:
                    self.spec_file[module].append(entity)
        for module in self.module_list:
            self.spec_file[module] = sorted(
                self.spec_file[module], key=lambda d: list(d.keys())
            )
        self.log.info("Spec file appended")

    def describe(self):
        """
        Provides a general description of the spesification.
        That can be used to validate the spesification.
        """
        description = Spessification_description()
        self.log.info("Describing spesification")
        for module in self.module_list:
            if module == "roles":
                description.load_module_description("roles", self.roles.describe())
                self.log.info("Roles described")
            elif module == "users":
                description.load_module_description("users", self.users.describe())
                self.log.info("Users described")
            elif module == "warehouses":
                description.load_module_description(
                    "warehouses", self.warehouses.describe()
                )
                self.log.info("Warehouses described")
            elif module == "databases":
                description.load_module_description(
                    "databases", self.databases.describe()
                )
                self.log.info("Databases described")
            else:
                self.log.error("Module not found")
                raise Exception("Module not found")
        self.log.info("Spesification described")
        return description

    def generate_roles(self):
        self.log.info("Start ipmutation of AR roles")
        self.log.info("generationg roles from Databases")
        accsess_roles_from_database = self.databases.generate_accsess_roles()
        self.roles.add_entities([accsess_roles_from_database])
        self.log.info("generationg roles from functional roles dependency")
        accsess_roles_from_functional_roles = self.roles.generate_accsess_roles()
        self.roles.add_entities([accsess_roles_from_functional_roles])
        self.log.info("identification of generated roles")
        self.identify_entities()

    def generate(self):
        if self.roles_generation == True:
            self.generate_roles()

        if self.verification == True:
            self.verify()

        self.output = ""
        self.log.info("Generating spec")
        generator = Permifrost_Spec_Generator("0.15.1")
        generator.generate(self.roles)
        self.log.info("Roles generated")
        generator.generate(self.users)
        self.log.info("Users generated")
        generator.generate(self.warehouses)
        self.log.info("Warehouses generated")
        generator.generate(self.databases)
        self.log.info("Databases generated")

        self.output = generator.get_output()
        self.generated = True
        self.log.info("Spec generation complete")
        self.log.debug("Generated spessification output:\n" + str(self.output))
        return self.output

    def export(self, file_name, writer=Yaml_file_Writer()):
        self.log.info("Exporting spec")
        self.log.debug("File name: " + str(file_name))
        if self.generated:
            writer.write(file_name, self.output)
            self.exported = True
            self.log.info("Spec exported")
        else:
            self.log.error("Spec not generated")
            raise Exception("Spec not generated")

    def verify(self):
        self.log.info("Verifying spec")
        self.verified = True
        recipet = []
        spec_verification = SpecVerification(self)
        self.log.info("Verifying databases")
        recipet.append(spec_verification.databases())
        self.log.info("Verifying warehouses")
        recipet.append(spec_verification.warehouses())
        self.log.info("Verifying users")
        recipet.append(spec_verification.users())
        self.log.info("Verifying roles")
        recipet.append(spec_verification.roles())

        if False in recipet:
            self.log.error("Spec verification failed")
            self.verified = False
            self.log.debug("Spec verification recipet: " + str(recipet))
            raise Exception("Spec verification failed")

        self.log.info("Spec verification complete")

    def get_state(self, module):
        if module == "roles":
            return self.roles.get_state()
        elif module == "users":
            return self.users.get_state()
        elif module == "warehouses":
            return self.warehouses.get_state()
        elif module == "databases":
            return self.databases.get_state()
        else:
            self.log.error("Module not found")
            raise Exception("Module not found")

    def get_entity(self, module, entity):
        if module == "roles":
            return self.roles.get_entities(entity)
        elif module == "users":
            return self.users.get_entities(entity)
        elif module == "warehouses":
            return self.warehouses.get_entities(entity)
        elif module == "databases":
            return self.databases.get_entities(entity)
        else:
            self.log.error("Module not found")
            return None
