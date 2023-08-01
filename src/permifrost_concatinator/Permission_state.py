import json
from src.permifrost_concatinator.Spesification import Spesification


class Permission_state:
    def __init__(self, specification: Spesification):
        self.serial = 0
        self.specification = specification
        self.state_file = None

    def generate(self):
        self.state_file = {}
        self.state_file["version"] = "0.1.0"
        self.state_file["serial"] = self.serial + 1
        self.state_file["generated"] = self.specification.roles_generation
        self.state_file["modules"] = {}
        for module in self.specification.module_list:
            self.state_file["modules"][module] = self.specification.get_state(module)

    def export(self, file_path: str):
        self.generate()
        try:
            with open(file_path, "w") as file:
                file.write(json.dumps(self.state_file, indent=4))
        except:
            with open(file_path, "x") as file:
                file.write(json.dumps(self.state_file, indent=4))
