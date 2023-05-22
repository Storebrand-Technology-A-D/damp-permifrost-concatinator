import pytest
import yaml
from src.Roles import Roles_Module


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


def test_roles_module_get_role(roles_loaded):
    assert roles_loaded.get_entities("role1") == {"member_of": ["role2"]}
    assert roles_loaded.get_entities("role2") == {
        "member_of": [
            "ar_db_database1_r",
            "ar_db_database1_w",
            "ar_db_database2_r",
            "ar_db_database2_w",
        ]
    }


def test_roles_module_get_role_not_found(roles_loaded):
    with pytest.raises(Exception):
        roles_loaded.get_entities("role3")


def test_roles_module_is_role(roles_loaded):
    assert roles_loaded.is_entity("role1") == True


def test_roles_module_is_role_not_found(roles_loaded):
    assert roles_loaded.is_entity("role3") == False


def test_roles_module_describe(roles_loaded):
    roles_description = roles_loaded.describe()
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


def test_roles_module_identify(roles_loaded):
    roles_loaded.identify_roles()
    assert set(roles_loaded.functional_roles) == set(["role1", "role2"])
    assert set(roles_loaded.functional_roles_dependencies) == set(
        [
            "role2",
            "ar_db_database1_r",
            "ar_db_database1_w",
            "ar_db_database2_r",
            "ar_db_database2_w",
        ]
    )
    assert set(roles_loaded.access_roles) == set(
        [
            "ar_db_database1_r",
            "ar_db_database1_w",
            "ar_db_database2_r",
            "ar_db_database2_w",
        ]
    )
