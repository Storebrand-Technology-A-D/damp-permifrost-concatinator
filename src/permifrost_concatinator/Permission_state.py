import json
import logging
import sys
from dictdiffer import diff
from dictdiffer.utils import PathLimit
from .Spesification import Spesification
from .txt_generator import txt_generator


class Permission_state:
    def __init__(self, specification: Spesification = None):
        self.serial = 0
        self.specification = specification
        self.state = None
        self.log = logging.getLogger(__name__)
        self.log.info("Creating Permission_state")
        self.txt = txt_generator(4)

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
        self.serial = self.state["serial"]
        return self

    def compare(self, comparative_state_file: "Permission_state"):
        self.log.info("Comparing state")
        state_diff = diff(
            comparative_state_file.state,
            self.state,
            path_limit=PathLimit(),
            ignore=["serial", "generated", "version"],
        )

        self.state_changes = []

        for difference in list(state_diff):
            self.log.debug(f"Difference: {difference}")
            self.log.info(f"{difference[0]} change in {difference[1]}")
            split_change = difference[1].split(".")
            if len(split_change) == 3:
                base, module, entity = split_change
                self.log.debug(f"Module: {module}, entity: {entity}")
                self.state_changes.append((module, entity)) if (
                    module,
                    entity,
                ) not in self.state_changes else self.state_changes
            elif len(split_change) == 2:
                base, module = split_change
                self.log.debug(f"Module: {module}, entity: {difference[2][0][0]}")
                if len(difference[2]) > 1:
                    for change in difference[2]:
                        self.log.debug(f"Change: {change}")
                        self.state_changes.append((module, change[0])) if (
                            module,
                            change[0],
                        ) not in self.state_changes else self.state_changes
                else:
                    self.state_changes.append((module, difference[2][0][0])) if (
                        module,
                        difference[2][0][0],
                    ) not in self.state_changes else self.state_changes

        return self

    def plan(self, file_path: str = None):
        if file_path is not '':
            with open(file_path, "w") as file:
                if len(self.state_changes) == 0:
                    self.log.info("No changes to apply")
                    file.write("No Changes\n")
                    return
                file.write("Changes to the following objects:\n")
                deletions = []
                self.log.info(f"Number of changes: {len(self.state_changes)}")
                self.log.debug(f"State changes: {self.state_changes}")
                for change in self.state_changes:
                    self.log.debug(f"Change: {change}")
                    self.log.debug(
                        f"Entity: {self.specification.get_entity(change[0], change[1])}"
                    )
                    self.log.debug(
                        f"type: {type(self.specification.get_entity(change[0], change[1]))}"
                    )
                    new_state = self.specification.get_entity(change[0], change[1])
                    if new_state is not None:
                        file.write(f"    {change[0]}: {change[1]}: {new_state}\n")
                    else:
                        self.log.debug(f"Entity: {change} to be deleted")
                        deletions.append(change)
                if len(deletions) > 0:
                    self.log.info(f"Number of deletions: {len(deletions)}")
                    self.log.debug(f"Deletions: {deletions}")
                    file.write("Entities to be removed:\n")
                    for deletion in deletions:
                        file.write(f"    {deletion[0]}: {deletion[1]}\n")
        else:
            if len(self.state_changes) == 0:
                self.log.info("No changes to apply")
                print("No Changes")
                return
            print("Changes to the following objects:")
            deletions = []
            self.log.info(f"Number of changes: {len(self.state_changes)}")
            self.log.debug(f"State changes: {self.state_changes}")
            for change in self.state_changes:
                self.log.debug(f"Change: {change}")
                self.log.debug(
                    f"Entity: {self.specification.get_entity(change[0], change[1])}"
                )
                self.log.debug(
                    f"type: {type(self.specification.get_entity(change[0], change[1]))}"
                )
                new_state = self.specification.get_entity(change[0], change[1])
                if new_state is not None:
                    print(f"    {change[0]}: {change[1]}: {new_state}")
                else:
                    self.log.debug(f"Entity: {change} to be deleted")
                    deletions.append(change)

            if len(deletions) > 0:
                self.log.info(f"Number of deletions: {len(deletions)}")
                self.log.debug(f"Deletions: {deletions}")
                print("Entities to be removed:")
                for deletion in deletions:
                    print(f"    {deletion[0]}: {deletion[1]}")

            return
