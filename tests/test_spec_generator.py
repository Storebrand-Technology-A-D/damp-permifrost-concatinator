from src.Spec_generator import Spec_Generator
from src.Users import Users_Module
from src.Warehouses import Warehouses_Module
from src.Databases import Databases_Module
from src.Roles import Roles_Module

from src.Spesification import Spesification

import pytest
space = " "*2


def load_yaml(yaml_file):
    with open(yaml_file, "r") as in_fh:
        file = yaml.safe_load(in_fh)
    return file

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
    database.spesification = {"database2": {"shared": "no", "owner": "loader_qlik"}}
    return database


@pytest.fixture
def databases_object():
    databases = Databases_Module()
    databases.spesification = {
        "database1": {"shared": "yes", "owner": "loader_qlik"},
        "database2": {"shared": "no", "owner": "loader_qlik"},
        "database3": {"shared": "yes"},
    }
    return databases


@pytest.fixture
def single_functional_role_object():
    functional_role = Roles_Module()
    functional_role.spesification = {
        "role2": {
            "warehouses": ["warehouse1"],
            "member_of": [
                "ar_db_database1_r",
                "ar_db_database1_w",
                "ar_db_database2_r",
                "ar_db_database2_w",
            ],
        }
    }
    functional_role.identify_roles()
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
    functional_roles.identify_roles()
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
    accsess_role.identify_roles()
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
                "databases": { "write": ["database1"]},
                "schemas": {"write": ["database1.*"]},
                "tables": {"write": ["database1.*.*"]},
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
    accsess_roles.identify_roles()
    return accsess_roles


@pytest.fixture
def roles_object():
    roles = Roles_Module()
    roles.spesification = {
        "role1": {"member_of": ["role2"]},
        "role2": {
            "member_of": [
                "ar_db_database1_r",
                "ar_db_database1_w",
                "ar_db_database2_r",
                "ar_db_database2_w",
            ]
        },
        "ar_db_database1_r": {
            "privileges": {
                "databases": {"read": ["database1"]},
                "schemas": {"read": ["database1.*"]},
                "tables": {"read": ["database1.*.*"]},
            }
        },
        "ar_db_database1_w": {
            "privileges": {
                "databases": {"write": ["database1"]},
                "schemas": {"write": ["database1.*"]},
                "tables": {"write": ["database1.*.*"]},
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
    roles.identify_roles()
    return roles


def test_spec_generator_singel_user_generator(singel_user_object):
    spec_generator = Spec_Generator("0.14.0")
    spec_generator.generate(singel_user_object)
    assert (
        spec_generator.users
        == f"""users:\n{space*1}- user1:\n{space*2}can_login: yes\n{space*2}member_of:\n{space*3}- role1\n"""
    )


def test_spec_generator_generate_users(users_object):
    spec_generator = Spec_Generator("0.14.0")
    spec_generator.generate(users_object)
    assert (
        spec_generator.users
        == f"""users:\n{space*1}- user1:\n{space*2}can_login: yes\n{space*2}member_of:\n{space*3}- role1\n{space*1}- user2:\n{space*2}can_login: yes\n{space*2}member_of:\n{space*3}- role2\n{space*1}- user3:\n{space*2}can_login: no\n{space*2}member_of:\n{space*3}- role3\n"""
    )


def test_spec_generator_generate_empty_users():
    users = Users_Module()
    spec_generator = Spec_Generator("0.14.0")
    spec_generator.generate(users)
    assert spec_generator.users == "users:\n"


def test_spec_generator_generate_single_database(single_database_object):
    spec_generator = Spec_Generator("0.14.0")
    spec_generator.generate(single_database_object)
    assert (
        spec_generator.databases
        == f"""databases:\n{space*1}- database2:\n{space*2}shared: no\n{space*2}owner: loader_qlik\n"""
    )


def test_spec_generator_generate_databases(databases_object):
    spec_generator = Spec_Generator("0.14.0")
    spec_generator.generate(databases_object)
    assert (
        spec_generator.databases
        == f"""databases:\n{space*1}- database1:\n{space*2}shared: yes\n{space*2}owner: loader_qlik\n{space*1}- database2:\n{space*2}shared: no\n{space*2}owner: loader_qlik\n{space*1}- database3:\n{space*2}shared: yes\n"""
    )


def test_spec_generator_generate_single_warehouse(single_warehouse_object):
    spec_generator = Spec_Generator("0.14.0")
    spec_generator.generate(single_warehouse_object)
    assert (
        spec_generator.warehouses
        == f"""warehouses:\n{space*1}- warehouse1:\n{space*2}size: xsmall\n"""
    )


def test_spec_generator_generate_warehouses(warehouses_object):
    spec_generator = Spec_Generator("0.14.0")
    spec_generator.generate(warehouses_object)
    assert (
        spec_generator.warehouses
        == f"""warehouses:\n{space*1}- warehouse1:\n{space*2}size: xsmall\n{space*1}- warehouse2:\n{space*2}size: xsmall\n{space*1}- warehouse3:\n{space*2}size: medium\n"""
    )


def test_spec_generator_generate_single_functional_role(single_functional_role_object):
    spec_generator = Spec_Generator("0.14.0")
    spec_generator.generate(single_functional_role_object)
    assert (
        spec_generator.functional_roles
        == f"""{space*1}- role2:\n{space*2}warehouses:\n{space*3}- warehouse1\n{space*2}member_of:\n{space*3}- ar_db_database1_r\n{space*3}- ar_db_database1_w\n{space*3}- ar_db_database2_r\n{space*3}- ar_db_database2_w\n\n""")

def test_spec_generator_generate_multiple_functional_roles(functional_roles_object):
    spec_generator = Spec_Generator("0.14.0")
    spec_generator.generate(functional_roles_object)
    assert (
        spec_generator.functional_roles
        == f"""{space*1}- role1:\n{space*2}member_of:\n{space*3}- role2\n{space*1}- role2:\n{space*2}member_of:\n{space*3}- ar_db_database1_r\n{space*3}- ar_db_database1_w\n{space*3}- ar_db_database2_r\n{space*3}- ar_db_database2_w\n\n""")


def test_spec_generator_generate_accsess_roles(single_accsess_role_object):
    spec_generator = Spec_Generator("0.14.0")
    spec_generator.generate(single_accsess_role_object)
    assert (
        spec_generator.access_roles
        == f"""{space*1}- ar_db_database1_r:\n{space*2}privileges:\n{space*3}databases:\n{space*4}read:\n{space*5}- database1\n{space*3}schemas:\n{space*4}read:\n{space*5}- database1.*\n{space*3}tables:\n{space*4}read:\n{space*5}- database1.*.*\n""" 
          )


def test_spec_generator_generate_multiple_accsess_roles(accsess_roles_object):
    spec_generator = Spec_Generator("0.14.0")
    spec_generator.generate(accsess_roles_object)
    assert (
        spec_generator.access_roles
        ==f"""{space*1}- ar_db_database1_r:\n{space*2}privileges:\n{space*3}databases:\n{space*4}read:\n{space*5}- database1\n{space*3}schemas:\n{space*4}read:\n{space*5}- database1.*\n{space*3}tables:\n{space*4}read:\n{space*5}- database1.*.*\n{space*1}- ar_db_database1_w:\n{space*2}privileges:\n{space*3}databases:\n{space*4}write:\n{space*5}- database1\n{space*3}schemas:\n{space*4}write:\n{space*5}- database1.*\n{space*3}tables:\n{space*4}write:\n{space*5}- database1.*.*\n{space*1}- ar_db_database2_r:\n{space*2}privileges:\n{space*3}databases:\n{space*4}read:\n{space*5}- database2\n{space*3}schemas:\n{space*4}read:\n{space*5}- database2.*\n{space*3}tables:\n{space*4}read:\n{space*5}- database2.*.*\n{space*1}- ar_db_database2_w:\n{space*2}privileges:\n{space*3}databases:\n{space*4}write:\n{space*5}- database2\n{space*3}schemas:\n{space*4}write:\n{space*5}- database2.*\n{space*3}tables:\n{space*4}write:\n{space*5}- database2.*.*\n""" 
    )

def test_spec_generator_generate_roles(roles_object):
    spec_generator = Spec_Generator("0.14.0")
    spec_generator.generate(roles_object)
    assert (
        spec_generator.roles
        ==f"""roles:\n{space*1}- role1:\n{space*2}member_of:\n{space*3}- role2\n{space*1}- role2:\n{space*2}member_of:\n{space*3}- ar_db_database1_r\n{space*3}- ar_db_database1_w\n{space*3}- ar_db_database2_r\n{space*3}- ar_db_database2_w\n\n{space*1}- ar_db_database1_r:\n{space*2}privileges:\n{space*3}databases:\n{space*4}read:\n{space*5}- database1\n{space*3}schemas:\n{space*4}read:\n{space*5}- database1.*\n{space*3}tables:\n{space*4}read:\n{space*5}- database1.*.*\n{space*1}- ar_db_database1_w:\n{space*2}privileges:\n{space*3}databases:\n{space*4}write:\n{space*5}- database1\n{space*3}schemas:\n{space*4}write:\n{space*5}- database1.*\n{space*3}tables:\n{space*4}write:\n{space*5}- database1.*.*\n{space*1}- ar_db_database2_r:\n{space*2}privileges:\n{space*3}databases:\n{space*4}read:\n{space*5}- database2\n{space*3}schemas:\n{space*4}read:\n{space*5}- database2.*\n{space*3}tables:\n{space*4}read:\n{space*5}- database2.*.*\n{space*1}- ar_db_database2_w:\n{space*2}privileges:\n{space*3}databases:\n{space*4}write:\n{space*5}- database2\n{space*3}schemas:\n{space*4}write:\n{space*5}- database2.*\n{space*3}tables:\n{space*4}write:\n{space*5}- database2.*.*\n"""  )


def test_spec_generator_generate_multiple_modules(databases_object, warehouses_object):

    module_list = [databases_object, warehouses_object]
    spec_generator = Spec_Generator("0.14.0")
    for spec in module_list:
        spec_generator.generate(spec)
    assert (
        spec_generator.get_output()
        == f"""version: "0.14.0"\ndatabases:\n{space*1}- database1:\n{space*2}shared: yes\n{space*2}owner: loader_qlik\n{space*1}- database2:\n{space*2}shared: no\n{space*2}owner: loader_qlik\n{space*1}- database3:\n{space*2}shared: yes\nwarehouses:\n{space*1}- warehouse1:\n{space*2}size: xsmall\n{space*1}- warehouse2:\n{space*2}size: xsmall\n{space*1}- warehouse3:\n{space*2}size: medium\n"""
    )