from src.Base_module import Base_Module
import logging


class Roles_Module(Base_Module):
    def __init__(self):
        self.spesification = {}
        self.type = "Role"
        self.log = logging.getLogger(__name__)

    def identify_roles(self):
        self.log.info("Identifying roles")
        self.functional_roles = []
        self.functional_roles_dependencies = []
        self.access_roles = []

        for role in self.spesification:
            self.log.info(f"Identifying role: {role}")
            if "privileges" in self.spesification[role]:
                self.log.debug(f"Role {role} is an access role")
                self.access_roles.append(role)
            elif "member_of" in self.spesification[role]:
                self.log.debug(f"Role {role} is a functional role")
                self.functional_roles.append(role)
                self.functional_roles_dependencies.extend(
                    dependency
                    for dependency in self.spesification[role]["member_of"]
                    if dependency not in self.functional_roles_dependencies
                )
