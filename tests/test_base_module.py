from src.permifrost_concatinator.Base_module import Base_Module
import pytest
import logging

def test_base_module_add_entities(object1):
    base_module = Base_Module()
    base_module.add_entities(object1)
    assert base_module.spesification == {
        "entitiy1": {"key": "value"},
        "entitiy2": {"key": "value"},
    }


def test_base_module_add_entities(object1, object2, base_module_loaded):
    base_module = Base_Module()
    base_module.add_entities(object1)
    base_module.add_entities(object2)
    assert base_module.spesification == base_module_loaded.spesification


def test_base_module_get_entitiy(base_module_loaded):
    assert base_module_loaded.get_entities("entitiy1") == {"key": "value"}


def test_base_module_get_entitiy_not_found(base_module_loaded):
    with pytest.raises(Exception) as exception_info:
        base_module_loaded.get_entities("entitiy4")
    assert exception_info.type == Exception
    assert exception_info.value.args[0] == "Entity not found"


def test_base_module_is_entitiy(base_module_loaded):
    assert base_module_loaded.is_entity("entitiy1") == True


def test_base_module_is_entitiy_not_found(base_module_loaded):
    assert base_module_loaded.is_entity("entitiy4") == False


def test_base_module_describe(base_module_loaded):
    description = base_module_loaded.describe()
    assert description.count == 3
    assert description.entities == ["entitiy1", "entitiy2", "entitiy3"]


def test_base_module_get_dependencies(
    base_module_loaded_with_dependencies, base_module_loaded
):
    assert base_module_loaded_with_dependencies.get_dependencies("member_of") == [
        "dependency1",
        "dependency2",
    ]
    assert base_module_loaded_with_dependencies.get_dependencies("warehouse") == [
        "dependency4"
    ]
    assert base_module_loaded.get_dependencies("key") == ["value"]


def test_base_module_get_dependencies_not_found(base_module_loaded_with_dependencies, caplog):
    caplog.set_level(logging.WARNING)
    base_module_loaded_with_dependencies.get_dependencies("not_a_dependency")
    assert "No not_a_dependency dependencies found in Entity" in caplog.text


def test_base_module_get_state(base_module_loaded):
    assert base_module_loaded.get_state() == {
        "entitiy1": {"key": "value"},
        "entitiy2": {"key": "value"},
        "entitiy3": {"key": "value"},
    }
