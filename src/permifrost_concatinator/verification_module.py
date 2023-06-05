import logging


class SpecVerification:
    def __init__(self, spec):
        self.spec = spec
        self.verified = False
        self.log = logging.getLogger(__name__)
        self.log.info("Spec verification initialized")

    def databases(self):
        self.log.info("Verifying databases")
        database_verified = True
        database_dependencies = self.spec.databases.get_dependencies("owner")
        for owner in database_dependencies:
            if owner not in self.spec.roles.functional_roles:
                self.log.error(
                    f"Role {owner} is a database owner, but is not a functional role"
                )
                database_verified = False
        return database_verified

    def users(self):
        self.log.info("Verifying users")
        user_verified = True
        user_dependencies = self.spec.users.get_dependencies("member_of")
        for role in user_dependencies:
            if role not in self.spec.roles.functional_roles:
                self.log.error(
                    f"Role {role} is assigned to a user, but is not a functional role"
                )
                user_verified = False
        return user_verified

    def warehouses(self):
        self.log.info("Verifying warehouses")
        warehouse_verified = True
        warehouse_dependencies = self.spec.warehouses.get_dependencies("owner")
        for owner in warehouse_dependencies:
            if owner not in self.spec.roles.functional_roles:
                self.log.error(
                    f"Role {owner} is a warehouse owner, but is not a functional role"
                )
                warehouse_verified = False
        return warehouse_verified

    def roles(self):
        self.log.info("Verifying roles")
        role_verified = True
        role_dependencies = self.spec.roles.get_dependencies("member_of")
        for role in role_dependencies:
            if role not in self.spec.roles.functional_roles:
                if role not in self.spec.roles.access_roles:
                    if role in ["aad_provisioner", "useradmin"]:
                        pass
                    else:
                        self.log.error(
                            f"Role {role} is assigned to a role, but is not defined as a role"
                        )
                        role_verified = False
        privilage_dependencies = self.spec.roles.get_databases()
        for database in privilage_dependencies:
            if database not in self.spec.databases.spesification:
                self.log.error(
                    f"Database {database} is assigned to a role, but is not a database"
                )
                role_verified = False
        warehouse_dependencies = self.spec.roles.get_dependencies("warehouse")
        for warehouse in warehouse_dependencies:
            if warehouse not in self.spec.warehouses.spesification:
                self.log.error(
                    f"Warehouse {warehouse} is assigned to a role, but is not a warehouse"
                )
                role_verified = False
        return role_verified
