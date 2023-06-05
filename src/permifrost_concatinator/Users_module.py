from .Base_module import Base_Module
import logging


class Users_Module(Base_Module):
    """
    Class for holding onto a permifrost users as imported from a spec file.

    """

    def __init__(self):
        self.spesification = {}
        self.type = "User"
        self.log = logging.getLogger(__name__)

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
