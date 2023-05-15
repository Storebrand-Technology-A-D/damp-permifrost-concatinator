from src.Spec_generator import Spec_Generator
from src.Users import Users_Module
from src.Warehouses import Warehouses_Module
from src.Databases import Databases_Module
from src.Roles import Roles_Module

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

@pytest.fixture
def single_warehouse_object():
    warehouse = Warehouses_Module()
    warehouse.spesification = {"warehouse1": {"size": "xsmall"}}
    return warehouse

@pytest.fixture
def warehouses_object():
    warehouses = Warehouses_Module()
    warehouses.spesification = {
        "warehouse1": {"size": "xsmall"},
        "warehouse2": {"size": "xsmall"},
        "warehouse3": {"size": "medium"},
    }
    return warehouses

@pytest.fixture
def single_database_object():
    database = Databases_Module()
    database.spesification = {"database2": {"shared": False, "owner": "loader_qlik"}},
    return database


@pytest.fixture
def databases_object(): 
    databases = Databases_Module()
    databases.spesification = {
        "database1": {"shared": True, "owner": "loader_qlik"},
        "database2": {"shared": False, "owner": "loader_qlik"},
        "database3": {"shared": True},
    }
    return databases

@pytest.fixture
def single_functional_role_object():
    functional_role = Roles_Module()
    functional_role.spesification = {"role2": {
                "member_of": [
                    "ar_db_database1_r",
                    "ar_db_database1_w",
                    "ar_db_database2_r",
                    "ar_db_database2_w",
                ]
            }
    }
    return functional_role

@pytest.fixture
def functional_roles_object():
    functional_roles = Roles_Module()
    functional_roles.spesification = {
        "role1": {"member_of": ["role2"]},
        "role2": {
            "member_of": [
                "ar_db_database1_r",
                "ar_db_database1_w",
                "ar_db_database2_r",
                "ar_db_database2_w",
            ]
        },
    }
    return functional_roles

@pytest.fixture
def single_accsess_role_object():
    accsess_role = Roles_Module()
    accsess_role.spesification = {
            "ar_db_database1_r": {
                "privileges": {
                    "databases": {"read": ["database1"]},
                    "schemas": {"read": ["database1.*"]},
                    "tables": {"read": ["database1.*.*"]},
                }
            }
        }
    return accsess_role

@pytest.fixture
def accsess_roles_object():
    accsess_roles = Roles_Module()
    accsess_roles.spesification = {
        "ar_db_database1_r": {
            "privileges": {
                "databases": {"read": ["database1"]},
                "schemas": {"read": ["database1.*"]},
                "tables": {"read": ["database1.*.*"]},
            }
        },
        "ar_db_database1_w": {
            "privileges": {
                "databases": {"read": ["database1"], "write": ["database1"]},
                "schemas": {"read": ["database1.*"], "write": ["database1.*"]},
                "tables": {"read": ["database1.*.*"], "write": ["database1.*.*"]},
            }
        },
        "ar_db_database2_r": {
            "privileges": {
                "databases": {"read": ["database2"]},
                "schemas": {"read": ["database2.*"]},
                "tables": {"read": ["database2.*.*"]},
            }
        },
        "ar_db_database2_w": {
            "privileges": {
                "databases": {"write": ["database2"]},
                "schemas": {"write": ["database2.*"]},
                "tables": {"write": ["database2.*.*"]},
            }
        },
    }
    return accsess_roles

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

def test_spec_generator_generate_single_warehouse(single_warehouse_object):
    spec_generator = Spec_Generator("0.14.0")
    spec_generator.generate(single_warehouse_object)
    assert spec_generator.output == """version: "0.14.0"\ndatabases:\n  - test_db:\n      owner: test_owner\n      warehouses:\n        - test_warehouse\n"""

def test_spec_generator_generate_single_database(single_database_object):
    spec_generator = Spec_Generator("0.14.0")
    spec_generator.generate(single_database_object)
    assert spec_generator.output == """version: "0.14.0"\ndatabases:\n  - database2:\n      owner: loader_qlik\n      shared: false\n"""