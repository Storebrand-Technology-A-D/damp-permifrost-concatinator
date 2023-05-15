from src.Base_module import Base_Module


class Roles_Module(Base_Module):
    def __init__(self):
        self.spesification = {}
        self.type = "Role"

    def identify_roles(self):
        self.functional_roles = []
        self.functional_roles_dependencies = []
        self.access_roles = []

        for role in self.spesification:
            if "privileges" in self.spesification[role]:
                self.access_roles.append(role)
            else:
                self.functional_roles.append(role)
                self.functional_roles_dependencies.extend(
                    dependency
                    for dependency in self.spesification[role]["member_of"]
                    if dependency not in self.functional_roles_dependencies
                )
