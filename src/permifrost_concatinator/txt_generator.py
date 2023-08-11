import logging


class txt_generator:
    def __init__(self, spaces=2):
        self.space = " " * spaces
        self.log = logging.getLogger(__name__)

    def generate_users(self, user, user_entity):
        result = ""
        result += f"""{self.space*1}- {user}:\n"""
        for key in user_entity:
            if key == "member_of":
                result += f"""{self.space*3}{key}:\n"""
                for role in user_entity[key]:
                    result += f"""{self.space*4}- {role}\n"""
            elif key == "can_login":
                result += f"""{self.space*3}{key}: {user_entity[key]}\n"""
        return result

    def generate_databases(self, database, database_entity):
        result = ""
        result += f"""{self.space*1}- {database}:\n"""
        for key in database_entity:
            if key == "owner":
                result += f"""{self.space*3}{key}: {database_entity[key]}\n"""
            elif key == "shared":
                result += f"""{self.space*3}{key}: {database_entity[key]}\n"""
        return result

    def generate_warehouses(self, warehouse, warehouse_entity):
        result = ""
        result += f"""{self.space*1}- {warehouse}:\n"""
        for key in warehouse_entity:
            result += f"""{self.space*3}{key}: {warehouse_entity[key]}\n"""
        return result

    def generate_accsess_role(self, role, role_entity):
        result = f"""{self.space*1}- {role}:\n"""
        for key in role_entity:
            if key == "privileges":
                result += f"""{self.space*3}{key}:\n"""
                for privilege in role_entity[key]:
                    result += f"""{self.space*4}{privilege}:\n"""
                    for read_write in role_entity[key][privilege]:
                        result += f"""{self.space*5}{read_write}:\n"""
                        for database in role_entity[key][privilege][read_write]:
                            result += f"""{self.space*6}- {database}\n"""
        return result

    def generate_functional_role(self, role, role_entity):
        result = f"""{self.space*1}- {role}:\n"""
        for key in role_entity:
            self.log.debug(f"Generating {key} for {role}")
            if key == "member_of":
                self.log.debug(f"Generating membership for {role}")
                if role_entity[key] != []:
                    result += f"""{self.space*3}{key}:\n"""
                    for role_accsess in role_entity[key]:
                        result += f"""{self.space*4}- {role_accsess}\n"""
                else:
                    result += f"""{self.space*3}{key}: []\n"""
            elif key == "warehouses":
                self.log.debug(f"adding warehouses for {role}")
                result += f"""{self.space*3}{key}:\n"""
                for warehouse in role_entity[key]:
                    self.log.debug(f"Generating {warehouse} for {role}")
                    result += f"""{self.space*4}- {warehouse}\n"""
        return result
