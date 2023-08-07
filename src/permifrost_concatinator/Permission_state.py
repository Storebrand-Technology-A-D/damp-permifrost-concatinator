import json
import logging
from dictdiffer import diff
from dictdiffer.utils import PathLimit
from .Spesification import Spesification


class Permission_state:
    def __init__(self, specification: Spesification = None):
        self.serial = 0
        self.specification = specification
        self.state = None
        self.log = logging.getLogger(__name__)
        self.log.info("Creating Permission_state")

    def generate(self):
        self.state = {}
        self.state["version"] = "0.1.0"
        self.state["serial"] = self.serial + 1
        self.state["generated"] = self.specification.roles_generation
        self.state["modules"] = {}
        for module in self.specification.module_list:
            self.state["modules"][module] = self.specification.get_state(module)
        return self

    def export(self, file_path: str):
        self.generate()
        try:
            with open(file_path, "w") as file:
                file.write(json.dumps(self.state, indent=4))
        except:
            with open(file_path, "x") as file:
                file.write(json.dumps(self.state, indent=4))

    def load(self, loader, file_path: str):
        json = loader("json")
        self.state = json.load(file_path)
        return self

    def compare(self, comparative_state_file: "Permission_state"):
        self.log.info("Comparing state")
        state_diff = diff(
            self.state,
            comparative_state_file.state,
            path_limit=PathLimit(),
            ignore=["serial", "generated", "version"],
        )

        changes = []

        for difference in list(state_diff):
            self.log.debug(f"Difference: {difference}")
            self.log.info(f"{difference[0]} change in {difference[1]}")
            changes.append(difference[1])

        self.state_changes = []

        for change in changes:
            self.log.info(f"Change: {change}")
            split_change = change.split(".")
            if len(split_change) == 3:
                base, module, entity = split_change
                self.log.debug(f"Module: {module}, entity: {entity}")
                self.state_changes.append((module, entity))

        return self
