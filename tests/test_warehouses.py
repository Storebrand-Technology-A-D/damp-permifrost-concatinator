from src.Warehouses_module import Warehouses_Module
import pytest


def test_warehouse_module_add_entities(warehouses_object1):
    warehouses = Warehouses_Module()
    warehouses.add_entities(warehouses_object1)
    assert warehouses.spesification == [
        {"warehouse1": {"size": "xsmall"}},
        {"warehouse2": {"size": "xsmall"}},
    ]


def test_warehouse_module_add_entities(
    warehouses_object1, warehouses_object2, warehouses_object
):
    warehouses = Warehouses_Module()
    warehouses.add_entities(warehouses_object1)
    warehouses.add_entities(warehouses_object2)
    assert warehouses.spesification == warehouses_object.spesification


def test_warehouse_module_get_warehouse(warehouses_object):
    assert warehouses_object.get_entities("warehouse1") == {"size": "xsmall"}


def test_warehouse_module_get_warehouse_not_found(warehouses_object):
    with pytest.raises(Exception) as exception_info:
        warehouses_object.get_entities("warehouse4")
    assert exception_info.type == Exception
    assert exception_info.value.args[0] == "Warehouse not found"


def test_warehouse_is_warehouse(warehouses_object):
    assert warehouses_object.is_entity("warehouse1") == True


def test_warehouse_is_warehouse_not_found(warehouses_object):
    assert warehouses_object.is_entity("warehouse4") == False


def test_warehouse_describe(warehouses_object):
    warehouse_description = warehouses_object.describe()
    assert warehouse_description.count == 3
    assert set(warehouse_description.entities) == set(
        ["warehouse1", "warehouse2", "warehouse3"]
    )


def test_warehouse_describe_empty():
    warehouses = Warehouses_Module()
    warehouse_description = warehouses.describe()
    assert warehouse_description.count == 0
    assert set(warehouse_description.entities) == set([])
