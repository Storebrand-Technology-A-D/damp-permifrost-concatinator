from src.permifrost_concatinator.Roles_module import Roles_Module
import pytest


def test_roles_module_add_entities(roles_object1):
    roles = Roles_Module()
    roles.add_entities(roles_object1)
    assert roles.spesification == {
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


def test_roles_module_get_role(roles_object):
    assert roles_object.get_entities("role1") == {"member_of": ["role2"]}
    assert roles_object.get_entities("role2") == {
        "member_of": [
            "ar_db_database1_r",
            "ar_db_database1_w",
            "ar_db_database2_r",
            "ar_db_database2_w",
        ]
    }


def test_roles_module_get_role_not_found(roles_object):
    with pytest.raises(Exception):
        roles_object.get_entities("role3")


def test_roles_module_is_role(roles_object):
    assert roles_object.is_entity("role1") == True


def test_roles_module_is_role_not_found(roles_object):
    assert roles_object.is_entity("role3") == False


def test_roles_module_describe(roles_object):
    roles_description = roles_object.describe()
    assert roles_description.count == 6
    assert set(roles_description.entities) == set(
        [
            "role1",
            "role2",
            "ar_db_database1_r",
            "ar_db_database1_w",
            "ar_db_database2_r",
            "ar_db_database2_w",
        ]
    )


def test_roles_module_identify(roles_object):
    roles_object.identify_roles()
    assert set(roles_object.functional_roles) == set(["role1", "role2"])
    assert set(roles_object.functional_roles_dependencies) == set(
        [
            "role2",
            "ar_db_database1_r",
            "ar_db_database1_w",
            "ar_db_database2_r",
            "ar_db_database2_w",
        ]
    )
    assert set(roles_object.access_roles) == set(
        [
            "ar_db_database1_r",
            "ar_db_database1_w",
            "ar_db_database2_r",
            "ar_db_database2_w",
        ]
    )


def test_roles_get_dependencies(roles_object):
    assert set(roles_object.get_dependencies("member_of")) == set(
        [
            "role2",
            "ar_db_database1_r",
            "ar_db_database1_w",
            "ar_db_database2_r",
            "ar_db_database2_w",
        ]
    )


def test_roles_get_databases(roles_object):
    assert set(roles_object.get_databases("ar_db_database1_r")) == set(["database1"])
    assert set(roles_object.get_databases()) == set(["database1", "database2"])


def test_roles_get_databases_not_found(roles_object):
    with pytest.raises(Exception) as exception_info:
        roles_object.get_databases("monkeydo")
    assert exception_info.value.args[0] == "Role monkeydo not found"


def test_roles_get_databases_not_accsess_roles(roles_object):
    with pytest.raises(Exception) as exception_info:
        roles_object.get_databases("role1")
        assert (
            exception_info.value.args[0]
            == "Role role1 is not an access role, and does not have databases"
        )
