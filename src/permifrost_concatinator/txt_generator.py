
class txt_generator:
    def __init__(self, spaces=2):
        self.space = " " * spaces

    def generate_users(self, user, user_entity):
        result = ""
        result += f"""{self.space*1}- {user}:\n"""
        for key in user_entity:
            if key == "member_of":
                result += f"""{self.space*3}{key}:\n"""
                for role in user_entity[key]:
                    result += f"""{self.space*4}- {role}\n"""
            elif key == "can_login":
                result += (
                        f"""{self.space*3}{key}: {user_entity[key]}\n"""
                )
        return result