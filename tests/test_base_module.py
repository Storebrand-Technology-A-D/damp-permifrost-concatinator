import pytest
from src.Base_module import Base_Module


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
