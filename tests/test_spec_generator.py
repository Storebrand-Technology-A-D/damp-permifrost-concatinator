import pytest
from src.permifrost_concatinator.Spec_generator import Spec_Generator
from src.permifrost_concatinator.Users_module import Users_Module


def test_spec_generator_singel_user_generator(
    singel_user_object, singel_user_object_str_result
):
    spec_generator = Spec_Generator("0.14.0")
    spec_generator.generate(singel_user_object)
    assert spec_generator.users == singel_user_object_str_result


def test_spec_generator_generate_users(users_object, users_object_str_results):
    spec_generator = Spec_Generator("0.14.0")
    spec_generator.generate(users_object)
    assert spec_generator.users == users_object_str_results


def test_spec_generator_generate_empty_users():
    users = Users_Module()
    spec_generator = Spec_Generator("0.14.0")
    spec_generator.generate(users)
    assert spec_generator.users == "users:\n"


def test_spec_generator_generate_single_database(
    single_database_object, single_database_object_str_results
):
    spec_generator = Spec_Generator("0.14.0")
    spec_generator.generate(single_database_object)
    assert spec_generator.databases == single_database_object_str_results


def test_spec_generator_generate_databases(
    databases_object, databases_object_str_results
):
    spec_generator = Spec_Generator("0.14.0")
    spec_generator.generate(databases_object)
    assert spec_generator.databases == databases_object_str_results


def test_spec_generator_generate_single_warehouse(
    single_warehouse_object, single_warehouse_object_str_results
):
    spec_generator = Spec_Generator("0.14.0")
    spec_generator.generate(single_warehouse_object)
    assert spec_generator.warehouses == single_warehouse_object_str_results


def test_spec_generator_generate_warehouses(
    warehouses_object, warehouses_object_str_results
):
    spec_generator = Spec_Generator("0.14.0")
    spec_generator.generate(warehouses_object)
    assert spec_generator.warehouses == warehouses_object_str_results


def test_spec_generator_generate_single_functional_role(
    single_functional_role_object, single_functional_role_object_str_results
):
    spec_generator = Spec_Generator("0.14.0")
    spec_generator.generate(single_functional_role_object)
    assert spec_generator.functional_roles == single_functional_role_object_str_results


def test_spec_generator_generate_multiple_functional_roles(
    functional_roles_object, functional_roles_object_str_results
):
    spec_generator = Spec_Generator("0.14.0")
    spec_generator.generate(functional_roles_object)
    assert spec_generator.functional_roles == functional_roles_object_str_results


def test_spec_generator_generate_accsess_roles(
    single_accsess_role_object, single_accsess_role_object_str_results
):
    spec_generator = Spec_Generator("0.14.0")
    spec_generator.generate(single_accsess_role_object)
    assert spec_generator.access_roles == single_accsess_role_object_str_results


def test_spec_generator_generate_multiple_accsess_roles(
    accsess_roles_object, accsess_roles_object_str_results
):
    spec_generator = Spec_Generator("0.14.0")
    spec_generator.generate(accsess_roles_object)
    assert spec_generator.access_roles == accsess_roles_object_str_results


def test_spec_generator_generate_roles(
    roles_object_identified, roles_object_str_results
):
    spec_generator = Spec_Generator("0.14.0")
    spec_generator.generate(roles_object_identified)
    assert spec_generator.roles == roles_object_str_results


def test_spec_generator_generate_multiple_modules(
    databases_object,
    warehouses_object,
    databases_object_str_results,
    warehouses_object_str_results,
):
    module_list = [databases_object, warehouses_object]
    spec_generator = Spec_Generator("0.14.0")
    for spec in module_list:
        spec_generator.generate(spec)
    assert (
        spec_generator.get_output()
        == f"""version: "0.14.0"\n"""
        + databases_object_str_results
        + warehouses_object_str_results
    )

@pytest.mark.skip(reason="Not implemented")
def test_spec_generator_singel_warehous_input():
    pass