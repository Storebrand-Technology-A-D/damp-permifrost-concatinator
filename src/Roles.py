class Roles_Module:
    def __init__(self):
        self.spesification = {}

    def add_entities(self, roles):
        for role in roles:
            self.spesification.update(role)

    def get_entities(self, role):
        if role not in self.spesification:
            raise Exception("Role not found")
        return self.spesification[role]

    def is_entity(self, role):
        return role in self.spesification

    def describe(self):
        self.count = len(self.spesification)
        self.entities = list(self.spesification.keys())
        return self

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
