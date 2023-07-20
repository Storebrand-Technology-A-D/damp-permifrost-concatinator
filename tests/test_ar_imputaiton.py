import pytest
from src.permifrost_concatinator.Roles_module import Roles_Module
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
    assert accsess_roles == {"ar_db_database2_w": {
                "privileges": {
                    "databases": {"write": ["database2"]},
                    "schemas": {"write": ["database2.*"]},
                    "tables": {"write": ["database2.*.*"]},
                }
            }}
    assert len(caplog.records) == 3 


@pytest.mark.skip(reason="not yet working on")
def test_functional_roles_and_accsess_roles(functional_roles_object, accsess_roles_object):
    accsess_roles = functional_roles_object.generate_accsess_roles()
    assert accsess_roles == accsess_roles_object.spesifications

@pytest.mark.skip(reason="not jet working on")
def test_dev_prod_accsess_roles(caplog, dev_prod_accsess_role_object):
    caplog.set_level(logging.ERROR)
    roles = Roles_Module()
    roles.spessification = {
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