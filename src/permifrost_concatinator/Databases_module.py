from .Base_module import Base_Module
import logging
import regex as re


class Databases_Module(Base_Module):
    def __init__(self):
        self.spesification = {}
        self.type = "Database"
        self.log = logging.getLogger(__name__)

    def __get_users(self):
        users = []
        self.log.info(f"Getting users from {self.type}s")
        for database in self.spesification:
            self.log.debug(f"Getting users from {self.type}: {database}")
            if "owner" in self.spesification[database]:
                self.log.debug(f"Adding owner: {self.spesification[database]['owner']}")
                users.append(self.spesification[database]["owner"])
                self.log.debug(f"Current users: {users}")
        return list(set(users))

    def generate_accsess_roles(self):
        self.log.info("Generating access roles from Databases")
        access_roles = {}
        for database in self.spesification:  # Assuming self.spesification contains database names
            self.log.debug(f"Generating access role from database: {database}")
            
            # Skip snowflake core databases
            if re.match("^snowflake.*", database):
                self.log.debug(f"Database {database} is a snowflake core database, skipping generation of access role")
                continue
            
            db_name = ""
            if re.match("^dev_.*", database):
                db_name = database[4:]
                prefix = "dev_ar_db"
            elif re.match("^qa_.*", database):
                db_name = database[3:]
                prefix = "qa_ar_db"
            elif re.match("^test_.*", database):
                db_name = database[5:]
                prefix = "test_ar_db"
            elif re.match("^preprod_.*", database):
                db_name = database[8:]
                prefix = "preprod_ar_db"
            else:
                db_name = database
                prefix = "ar_db"
            
            if db_name:
                access_roles[f"{prefix}_{db_name}_w"] = {
                    "privileges": {
                        "databases": {"write": [f"{database}"]},
                        "schemas": {"write": [f"{database}.*"]},
                        "tables": {"write": [f"{database}.*.*"]},
                    }
                }
                access_roles[f"{prefix}_{db_name}_r"] = {
                    "privileges": {
                        "databases": {"read": [f"{database}"]},
                        "schemas": {"read": [f"{database}.*"]},
                        "tables": {"read": [f"{database}.*.*"]},
                    }
                }
        
        return access_roles


