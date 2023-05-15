
class Spec_Generator():
    def __init__(self, version):
        self.output = ""
        self.users = "\n"
        self.databases = "\n"

        self.version = version

    def generate_users(self, module):
        self.users = "users:\n"
        for user in module.spesification:
            self.users += f"""  - {user}:\n"""
            for key in module.spesification[user]:
                if key == "member_of":
                    self.users += f"""      {key}:\n"""
                    for role in module.spesification[user][key]:
                        self.users += f"""        - {role}\n"""
                elif key == "can_login":
                    self.users += f"""      {key}: {module.spesification[user][key]}\n"""

    def generate(self, module):
        self.output += f"""version: \"{self.version}\"\n"""
        if module.type == "User":
            self.generate_users(module)

        self.output += self.users