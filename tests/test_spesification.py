import pytest
import yaml
import logging
import os

from src.permifrost_concatinator.Spesification import Spesification


def test_spessification_load_spec_file(yaml_spessification_a):
    spesification = Spesification()
    spesification.load("tests/data/base_premissions/team_a_permisions.yml")
    assert spesification.spec_file == yaml_spessification_a


def test_spesification_module_identify(spesification_object_a):
    spesification_object_a.identify_modules()
    assert set(spesification_object_a.module_list) == set(
        ["roles", "users", "warehouses", "databases"]
    )


def test_spesification_identify_entities(spesification_object_a):
    spesification_object_a.identify_modules()
    load_confirmation = spesification_object_a.identify_entities()
    assert load_confirmation == True


def test_spesification_describe(spesification_object_a):
    spesification_object_a.identify_modules()
    spesification_object_a.identify_entities()
    description = spesification_object_a.describe()
    assert description.databases.keys() == {"count", "entities"}
    assert description.roles.keys() == {"count", "entities"}
    assert description.users.keys() == {"count", "entities"}


def test_spesification_append_spec(spesification_object_a, yaml_spessification_b):
    spesification_object_a.identify_modules()
    spesification_object_a.identify_entities()
    pre_description = spesification_object_a.describe()
    spesification_object_a.append_spec(yaml_spessification_b)
    post_description = spesification_object_a.describe()
    assert (
        pre_description.databases["entities"] != post_description.databases["entities"]
    )
    assert pre_description.databases["count"] < post_description.databases["count"]
    assert pre_description.roles["entities"] != post_description.roles["entities"]
    assert pre_description.users["entities"] == post_description.users["entities"]
    assert (
        pre_description.warehouses["entities"]
        == post_description.warehouses["entities"]
    )


def test_Spesification_generate(spesification_object_a):
    spesification_object_a.identify_modules()
    spesification_object_a.identify_entities()
    spesification_object_a.generate()
    assert spesification_object_a.generated == True
    assert isinstance(spesification_object_a.output, str)
    assert spesification_object_a.output != ""


def test_spesification_export(spesification_object_a):
    spesification_object_a.identify_modules()
    spesification_object_a.identify_entities()
    spesification_object_a.generate()
    spesification_object_a.export("exported.yml")
    with open("exported.yml", "r") as file:
        output = file.read()
    assert output == spesification_object_a.output
    try:
        os.remove("exported.yml")
    except FileNotFoundError:
        pass


def test_verify_spec_failing(spesification_team_c, caplog):
    caplog.set_level(logging.ERROR)
    with pytest.raises(Exception) as exception_info:
        spesification_team_c.verify()
        assert exception_info.value.args[0] == "Spec verification failed"
    assert spesification_team_c.verified == False
    assert len(caplog.records) == 7


def test_verify_spec_passing(spesification_team_c_verified, caplog):
    caplog.set_level(logging.ERROR)
    spesification_team_c_verified.verify()
    assert spesification_team_c_verified.verified == True
    assert len(caplog.records) == 0


def test_role_generation_from_databases(spesification_without_ar_roles, caplog):
    caplog.set_level(logging.DEBUG)
    spesification_without_ar_roles.generate_roles()
    assert spesification_without_ar_roles.roles.is_entity("ar_db_database1_r") == True


def test_role_generation_from_depencies(spesification_without_ar_roles):
    pass


def test_role_generation_combined_databases_dependencies(
    spesification_without_ar_roles,
):
    pass


def test_role_generation_missig_databases():
    pass


def test_role_generation_missing_dependencies():
    pass


def test_spessification_get_state(
    spesification_team_c_verified, team_c_verefied_state_file
):
    user_state = spesification_team_c_verified.get_state("users")
    assert user_state == team_c_verefied_state_file["modules"]["users"]
    role_state = spesification_team_c_verified.get_state("roles")
    assert role_state == team_c_verefied_state_file["modules"]["roles"]
    database_state = spesification_team_c_verified.get_state("databases")
    assert database_state == team_c_verefied_state_file["modules"]["databases"]
    warehouse_state = spesification_team_c_verified.get_state("warehouses")
    assert warehouse_state == team_c_verefied_state_file["modules"]["warehouses"]
