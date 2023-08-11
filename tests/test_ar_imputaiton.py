import pytest
from src.permifrost_concatinator.Roles_module import Roles_Module
from src.permifrost_concatinator.Spesification import Spesification
import logging


def test_generate_ar_from_db(databases_object, accsess_roles_object):
    databases_object.spesification.pop(
        "database3"
    )  # removed to match accsess_roles_object.spesification
    accsess_roles = databases_object.generate_accsess_roles()
    assert accsess_roles == accsess_roles_object.spesification


def test_generate_ar_from_functional_roles(
    accsess_roles_object, single_functional_role_object
):
    accsess_roles = single_functional_role_object.generate_accsess_roles()
    assert accsess_roles == accsess_roles_object.spesification


def test_malformed_ar_roles(caplog):
    caplog.set_level(logging.ERROR)
    roles = Roles_Module()
    roles.spesification = {
        "role2": {
            "warehouses": ["warehouse1"],
            "member_of": [
                "ar_db_database1_q",
                "ax_db_database1_w",
                "ar_Schema_database2_r",
                "ar_db_database2_w",
            ],
        }
    }
    roles.identify_roles()
    accsess_roles = roles.generate_accsess_roles()
    assert accsess_roles == {
        "ar_db_database2_w": {
            "privileges": {
                "databases": {"write": ["database2"]},
                "schemas": {"write": ["database2.*"]},
                "tables": {"write": ["database2.*.*"]},
            }
        }
    }
    assert len(caplog.records) == 3


def test_functional_roles_and_accsess_roles(
    functional_roles_object, accsess_roles_object
):
    accsess_roles = functional_roles_object.generate_accsess_roles()
    assert accsess_roles == accsess_roles_object.spesification


def test_dev_prod_accsess_roles(caplog, dev_prod_accsess_role_object):
    caplog.set_level(logging.ERROR)
    resultant_roles = set(
        {
            "ar_db_database1_w": {
                "privileges": {
                    "databases": {"write": ["database2"]},
                    "schemas": {"write": ["database2.*"]},
                    "tables": {"write": ["database2.*.*"]},
                }
            },
            "ar_db_database1_r": {
                "privileges": {
                    "databases": {"read": ["database1"]},
                    "schemas": {"read": ["database1.*"]},
                    "tables": {"read": ["database1.*.*"]},
                }
            },
            "dev_ar_db_database2_w": {
                "privileges": {
                    "databases": {"write": ["dev_database2"]},
                    "schemas": {"write": ["dev_database2.*"]},
                    "tables": {"write": ["dev_database2.*.*"]},
                }
            },
            "dev_ar_db_database2_r": {
                "privileges": {
                    "databases": {"read": ["dev_database2"]},
                    "schemas": {"read": ["dev_database2.*"]},
                    "tables": {"read": ["dev_database2.*.*"]},
                }
            },
        }
    )
    roles = Roles_Module()
    roles.spesification = {
        "role2": {
            "warehouses": ["warehouse1"],
            "member_of": [
                "ar_db_database1_r",
                "ar_db_database1_w",
                "dev_ar_db_database2_r",
                "dev_ar_db_database2_w",
            ],
        }
    }

    roles.identify_roles()
    accsess_roles = roles.generate_accsess_roles()
    assert set(accsess_roles) == resultant_roles

def test_dev_roles_from_databases_and_functional_roles(
        caplog,
    ):
        caplog.set_level(logging.ERROR)
        spec = Spesification(verification=True, generate_roles=True)
        spec.load("tests/data/dev_databases_and_roles.yml")
        spec.identify_modules()
        spec.identify_entities()
        spec.generate()
        assert set(spec.roles.access_roles) == set(
            {
            "dev_ar_db_database1_w": {
                "privileges": {
                    "databases": {"write": ["dev_database2"]},
                    "schemas": {"write": ["dev_database2.*"]},
                    "tables": {"write": ["dev_database2.*.*"]},
                }
            },
            "dev_ar_db_database1_r": {
                "privileges": {
                    "databases": {"read": ["dev_database1"]},
                    "schemas": {"read": ["dev_database1.*"]},
                    "tables": {"read": ["dev_database1.*.*"]},
                }
            },
            "dev_ar_db_database2_w": {
                "privileges": {
                    "databases": {"write": ["dev_database2"]},
                    "schemas": {"write": ["dev_database2.*"]},
                    "tables": {"write": ["dev_database2.*.*"]},
                }
            },
            "dev_ar_db_database2_r": {
                "privileges": {
                    "databases": {"read": ["dev_database2"]},
                    "schemas": {"read": ["dev_database2.*"]},
                    "tables": {"read": ["dev_database2.*.*"]},
                }
            },
            "ar_db_database4_w": {
                "privileges": {
                    "databases": {"write": ["database4"]},
                    "schemas": {"write": ["database4.*"]},
                    "tables": {"write": ["database4.*.*"]},
                }
            },
            "ar_db_database4_r": {
                "privileges": {
                    "databases": {"read": ["database4"]},
                    "schemas": {"read": ["database4.*"]},
                    "tables": {"read": ["database4.*.*"]},
                }
            },
            "ar_db_database5_w": {
                "privileges": {
                    "databases": {"write": ["database5"]},
                    "schemas": {"write": ["database5.*"]},
                    "tables": {"write": ["database5.*.*"]},
                }
            },
            "ar_db_database5_r": {
                "privileges": {
                    "databases": {"read": ["database5"]},
                    "schemas": {"read": ["database5.*"]},
                    "tables": {"read": ["database5.*.*"]},
                }
            }
        }
        )
