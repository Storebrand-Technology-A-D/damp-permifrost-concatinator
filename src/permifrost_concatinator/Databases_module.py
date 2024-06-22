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
        for database in self.spesification:  # Assuming self.specification contains database names
            self.log.debug(f"Generating access role from database: {database}")
            
            # Skip snowflake core databases
            if re.match("^snowflake.*", database):
                self.log.debug(f"Database {database} is a snowflake core database, skipping generation of access role")
                continue
            
            # Handle development databases (dev_)
            elif re.match("^dev_.*", database):
                self.log.debug(f"Database {database} is a development database, generating roles")
                db_name = database[4:]  # Extract the database name without the prefix
                
                # Write role
                access_roles[f"dev_ar_db_{db_name}_w"] = {
                    "privileges": {
                        "databases": {"write": [f"{database}"]},
                        "schemas": {"write": [f"{database}.*"]},
                        "tables": {"write": [f"{database}.*.*"]},
                    }
                }
                
                # Read role
                access_roles[f"dev_ar_db_{db_name}_r"] = {
                    "privileges": {
                        "databases": {"read": [f"{database}"]},
                        "schemas": {"read": [f"{database}.*"]},
                        "tables": {"read": [f"{database}.*.*"]},
                    }
                }
                     
            # Handle QA databases (qa_)
            elif re.match("^qa_.*", database):
                self.log.debug(f"Database {database} is a QA database, generating roles")
                db_name = database[3:]  # Extract the database name without the prefix
                
                # Write role
                access_roles[f"qa_ar_db_{db_name}_w"] = {
                    "privileges": {
                        "databases": {"write": [f"{database}"]},
                        "schemas": {"write": [f"{database}.*"]},
                        "tables": {"write": [f"{database}.*.*"]},
                    }
                }
                
                # Read role
                access_roles[f"qa_ar_db_{db_name}_r"] = {
                    "privileges": {
                        "databases": {"read": [f"{database}"]},
                        "schemas": {"read": [f"{database}.*"]},
                        "tables": {"read": [f"{database}.*.*"]},
                    }
                }
            
            # Handle Test databases (test_)
            elif re.match("^test_.*", database):
                self.log.debug(f"Database {database} is a Test database, generating roles")
                db_name = database[5:]  # Extract the database name without the prefix
                
                # Write role
                access_roles[f"test_ar_db_{db_name}_w"] = {
                    "privileges": {
                        "databases": {"write": [f"{database}"]},
                        "schemas": {"write": [f"{database}.*"]},
                        "tables": {"write": [f"{database}.*.*"]},
                    }
                }
                
                # Read role
                access_roles[f"test_ar_db_{db_name}_r"] = {
                    "privileges": {
                        "databases": {"read": [f"{database}"]},
                        "schemas": {"read": [f"{database}.*"]},
                        "tables": {"read": [f"{database}.*.*"]},
                    }
                }
            
            # Handle Preprod databases (preprod_)
            elif re.match("^preprod_.*", database):
                self.log.debug(f"Database {database} is a Preprod database, generating roles")
                db_name = database[8:]  # Extract the database name without the prefix
                
                # Write role
                access_roles[f"preprod_ar_db_{db_name}_w"] = {
                    "privileges": {
                        "databases": {"write": [f"{database}"]},
                        "schemas": {"write": [f"{database}.*"]},
                        "tables": {"write": [f"{database}.*.*"]},
                    }
                }
                
                # Read role
                access_roles[f"preprod_ar_db_{db_name}_r"] = {
                    "privileges": {
                        "databases": {"read": [f"{database}"]},
                        "schemas": {"read": [f"{database}.*"]},
                        "tables": {"read": [f"{database}.*.*"]},
                    }
                }
                   # Handle production databases 
            elif re.match("^ar_.*", database):
                self.log.debug(f"Database {database} is a production database, generating roles")
                db_name = database[3:]  # Extract the database name without the prefix
                
                # Write role
                access_roles[f"ar_db_{db_name}_w"] = {
                    "privileges": {
                        "databases": {"write": [f"{database}"]},
                        "schemas": {"write": [f"{database}.*"]},
                        "tables": {"write": [f"{database}.*.*"]},
                    }
                }
                
                # Read role
                access_roles[f"ar_db_{db_name}_r"] = {
                    "privileges": {
                        "databases": {"read": [f"{database}"]},
                        "schemas": {"read": [f"{database}.*"]},
                        "tables": {"read": [f"{database}.*.*"]},
                    }
                }    
        
        return access_roles


