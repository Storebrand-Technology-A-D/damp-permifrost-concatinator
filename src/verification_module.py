import logging


class SpecVerification:
    def __init__(self, spec):
        self.spec = spec
        self.verified = False
        self.log = logging.getLogger(__name__)
        self.log.info("Spec verification initialized")

    def databases(self):
        self.log.info("Verifying databases")
        database_dependencies = self.spec.databases.get_dependencies("owner")
        for owner in database_dependencies:
            if owner not in self.spec.roles.functional_roles:
                self.log.error(
                    f"Role {owner} is a database owner, but is not a functional role"
                )
                return False
        return True

    def users(self):
        self.log.info("Verifying users")
        user_dependencies = self.spec.users.get_dependencies("member_of")
        for role in user_dependencies:
            if role not in self.spec.roles.functional_roles:
                self.log.error(
                    f"Role {role} is assigned to a user, but is not a functional role"
                )
                return False
        return True
    
    def warehouses(self):
        self.log.info("Verifying warehouses")
        warehouse_dependencies = self.spec.warehouses.get_dependencies("owner")
        for owner in warehouse_dependencies:
            if owner not in self.spec.roles.functional_roles:
                self.log.error(
                    f"Role {owner} is a warehouse owner, but is not a functional role"
                )
                return False
        return True
    
    def roles(self):
        self.log.info("Verifying roles")
        role_dependencies = self.spec.roles.get_dependencies("member_of")
        for role in role_dependencies:
            if role not in self.spec.roles.functional_roles:
                if role not in self.spec.roles.access_roles:
                    self.log.error(
                        f"Role {role} is assigned to a role, but is not defined as a role"
                    )
                    return False
        privilage_dependencies = self.spec.roles.get_databases()
        for database in privilage_dependencies:
            if database not in self.spec.databases.spesification:
                self.log.error(
                    f"Database {database} is assigned to a role, but is not a database"
                )
                return False
        warehouse_dependencies = self.spec.roles.get_dependencies("warehouse")
        for warehouse in warehouse_dependencies:
            if warehouse not in self.spec.warehouses.spesification:
                self.log.error(
                    f"Warehouse {warehouse} is assigned to a role, but is not a warehouse"
                )
                return False
        return True