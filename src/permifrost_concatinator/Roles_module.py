from .Base_module import Base_Module
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

    def get_databases(self, role=None):
        if role is None:
            roles = self.spesification
            self.log.info(f"Getting databases for all roles")
        else:
            roles = [role]
            self.log.info(f"Getting databases for role: {role}")
        privileges = []
        for role in roles:
            if role not in self.spesification:
                self.log.error(f"Role {role} not found")
                raise Exception(f"Role {role} not found")
            elif len(role) == 1 and "privileges" not in self.spesification[role]:
                self.log.error(
                    f"Role {role} is not an access role, and does not have databases"
                )
                raise Exception(
                    f"Role {role} is not an access role, and does not have databases"
                )

            elif "privileges" in self.spesification[role]:
                self.log.debug(f"Role {role} is an access role")
                self.log.debug(
                    f"Privileges for role {role}: {self.spesification[role]['privileges']}"
                )
                try:
                    privileges.extend(
                        self.spesification[role]["privileges"]["databases"]["read"]
                    )
                except KeyError:
                    pass
                try:
                    privileges.extend(
                        self.spesification[role]["privileges"]["databases"]["write"]
                    )
                except KeyError:
                    pass
        self.log.debug(f"Databases for roles: {privileges}")
        self.log.info(f"Databases for roles retrieved from spec")
        return privileges
