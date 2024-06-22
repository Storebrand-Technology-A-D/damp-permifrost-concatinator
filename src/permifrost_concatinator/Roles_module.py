from .Base_module import Base_Module
import logging
import regex as re


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

    #def generate_accsess_roles(self):
    #    accsess_roles = {}
    #    self.log.info("Generating accsess roles")
    #    self.log.debug(f"Functional roles: {self.functional_roles_dependencies}")
    #    for role in self.functional_roles_dependencies:
    #        self.log.info(f"Generating accsess role for functional role: {role}")
    #        if re.match("ar_db_.*_(w|r)$", role):
    #            if re.match("^ar_db.*", role):
    #                database = role[6:-2]
    #                if re.match(".*_w$", role):
    #                   accsess_roles[role] = {
    #                        "privileges": {
    #                            "databases": {"write": [f"{database}"]},
    #                            "schemas": {"write": [f"{database}.*"]},
    #                            "tables": {"write": [f"{database}.*.*"]},
    #                        }
    #                    }
    #                else:
    #                    accsess_roles[role] = {
    #                        "privileges": {
    #                            "databases": {"read": [f"{database}"]},
    #                            "schemas": {"read": [f"{database}.*"]},
    #                            "tables": {"read": [f"{database}.*.*"]},
    #                        }
    #                    }
    #        elif re.match("^dev_ar_db.*_(w|r)$", role):
    #            database = role[10:-2]
    #            if re.match(".*_w$", role):
    #                accsess_roles[role] = {
    #                    "privileges": {
    #                        "databases": {"write": [f"dev_{database}"]},
    #                        "schemas": {"write": [f"dev_{database}.*"]},
    #                        "tables": {"write": [f"dev_{database}.*.*"]},
    #                    }
    #                }
    #            else:
    #                accsess_roles[role] = {
    #                    "privileges": {
    #                        "databases": {"read": [f"dev_{database}"]},
    #                        "schemas": {"read": [f"dev_{database}.*"]},
    #                        "tables": {"read": [f"dev_{database}.*.*"]},
    #                    }
    #                }
    #        elif re.match("^ar_schema.*_r$", role):
    #            next
#
#            elif re.match("ar_|_db_|.*_(r|w)$", role):
#                self.log.error(f"Malformed Accsess roles: {role}")


def generate_access_roles(self):
    access_roles = {}
    self.log.info("Generating access roles")
    self.log.debug(f"Functional roles: {self.functional_roles_dependencies}")

    # Define the patterns to match different types of roles
    patterns = [
        (r"^(ar_db_.+?)_(w|r)$", 6, 2, ""),          # Production databases (ar_db_name_r or ar_db_name_w)
        (r"^(dev_ar_db_.+?)_(w|r)$", 10, 2, "dev_"), # Development databases (dev_ar_db_name_r or dev_ar_db_name_w)
        (r"^(qa_ar_db_.+?)_(w|r)$", 9, 2, "qa_"),    # QA databases (qa_ar_db_name_r or qa_ar_db_name_w)
        (r"^(test_ar_db_.+?)_(w|r)$", 11, 2, "test_"), # Test databases (test_ar_db_name_r or test_ar_db_name_w)
        (r"^(preprod_ar_db_.+?)_(w|r)$", 14, 2, "preprod_") # Preprod databases (preprod_ar_db_name_r or preprod_ar_db_name_w)
    ]

    for role in self.functional_roles_dependencies:
        self.log.info(f"Generating access role for functional role: {role}")

        for pattern, db_start, db_end, prefix in patterns:
            match = re.match(pattern, role)
            if match:
                database = role[db_start:-db_end]
                db_prefix = f"{prefix}{database}"
                access_type = "write" if role.endswith("_w") else "read"
                access_roles[role] = {
                    "privileges": {
                        "databases": {access_type: [db_prefix]},
                        "schemas": {access_type: [f"{db_prefix}.*"]},
                        "tables": {access_type: [f"{db_prefix}.*.*"]}
                    }
                }
                break
        else:
            if re.match("^ar_schema.*_r$", role):
                continue
            elif re.match("ar_|_db_|.*_(r|w)$", role):
                self.log.error(f"Malformed Access roles: {role}")

    return access_roles

        return accsess_roles
