import pytest
from src.Users import Users_Module


@pytest.fixture
def user_object1():
    return [
        {"user1": {"can_login": True, "member_of": ["role1"]}},
        {"user2": {"can_login": True, "member_of": ["role2"]}},
    ]


@pytest.fixture
def user_object2():
    return [
        {"user3": {"can_login": False, "member_of": ["role3"]}},
        {"user2": {"can_login": True, "member_of": ["role2"]}},
    ]


@pytest.fixture
def users_loaded():
    users = Users_Module()
    users.spesification = {
        "user1": {"can_login": True, "member_of": ["role1"]},
        "user2": {"can_login": True, "member_of": ["role2"]},
        "user3": {"can_login": False, "member_of": ["role3"]},
    }
    return users


def test_user_add_users(user_object1):
    users = Users_Module()
    users.add_entities(user_object1)
    assert users.spesification == {
        "user1": {"can_login": True, "member_of": ["role1"]},
        "user2": {"can_login": True, "member_of": ["role2"]},
    }


def test_user_append_users(user_object1, user_object2, users_loaded):
    users = Users_Module()
    users.add_entities(user_object1)
    users.add_entities(user_object2)
    assert users.spesification == users_loaded.spesification


def test_users_get_user(users_loaded):
    assert users_loaded.get_entities("user1") == {"can_login": True, "member_of": ["role1"]}


def test_users_get_user_not_found(users_loaded):
    with pytest.raises(Exception) as exception_info:
        users_loaded.get_entities("user4")
    assert exception_info.type == Exception
    assert exception_info.value.args[0] == "User not found"


def test_users_is_user(users_loaded):
    assert users_loaded.is_entity("user1") == True


def test_users_is_user_not_found(users_loaded):
    assert users_loaded.is_entity("user4") == False


def test_users_describe(users_loaded):
    user_description = users_loaded.describe()
    assert user_description.count == 3
    assert set(user_description.entities) == set(["user1", "user2", "user3"])


def test_users_describe_empty():
    users = Users_Module()
    user_description = users.describe()
    assert user_description.count == 0
    assert user_description.entities == []
