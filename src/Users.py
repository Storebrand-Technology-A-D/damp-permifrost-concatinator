from .Module_description import Module_description
class Users_Module:
    """
    Class for holding onto a permifrost users as imported from a spec file.

    """

    def __init__(self):
        self.spesification = {}

    def add_entities(self, users):
        """
        Add users to the users object.
        """
        for user in users:
            self.spesification.update(user)

    def get_user(self, user):
        """
        Get a user from the users object.
        """
        if user not in self.spesification:
            raise Exception("User not found")

        return self.spesification[user]

    def is_user(self, user):
        """
        Check if user is in the users object.
        """
        return user in self.spesification

    def __get_roles(self):
        """
        Get all roles from the users object.
        """
        roles = []
        for user in self.spesification:
            roles.extend(self.spesification[user]["member_of"])
        return list(set(roles))

    def __get_login(self, yes_no):
        """
        Get all users that can login from the users object.
        """
        users = []
        for user in self.spesification:
            if self.spesification[user]["can_login"] == yes_no:
                users.append(user)
        return users

    def describe(self):
        """
        Provides a general description of the users object.
        That can be used to validate the spesification.
        """
        
        description = Module_description("users")
        description.gather_description(self)
        return description