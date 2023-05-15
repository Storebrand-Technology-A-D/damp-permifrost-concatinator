from src.Spec_generator import Spec_Generator
from src.Spesification import Spesification
from src.Users import Users_Module
import pytest


@pytest.fixture
def users_object():
    users = Users_Module()
    users.spesification = {
        "user1": {"can_login": "yes", "member_of": ["role1"]},
        "user2": {"can_login": "yes", "member_of": ["role2"]},
        "user3": {"can_login": "no", "member_of": ["role3"]},
    }
    return users


@pytest.fixture
def singel_user_object():
    users = Users_Module()
    users.spesification = {
        "user1": {"can_login": "yes", "member_of": ["role1"]},
    }
    return users


def test_spec_generator_singel_user_generator(singel_user_object):
    spec_generator = Spec_Generator("0.14.0")
    spec_generator.generate(singel_user_object)
    assert (
        spec_generator.output
        == """version: \"0.14.0\"\nusers:\n  - user1:\n      can_login: yes\n      member_of:\n        - role1\n"""
    )


def test_spec_generator_generate_users(users_object):
    spec_generator = Spec_Generator("0.14.0")
    spec_generator.generate(users_object)
    assert (
        spec_generator.output
        == """version: \"0.14.0\"\nusers:\n  - user1:\n      can_login: yes\n      member_of:\n        - role1\n  - user2:\n      can_login: yes\n      member_of:\n        - role2\n  - user3:\n      can_login: no\n      member_of:\n        - role3\n"""
    )

def test_spec_generator_generate_empty_users():
    users = Users_Module()
    spec_generator = Spec_Generator("0.14.0")
    spec_generator.generate(users)
    assert spec_generator.output == "version: \"0.14.0\"\nusers:\n"