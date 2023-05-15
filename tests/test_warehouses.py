import pytest
from src.Warehouses import Warehouses_Module


@pytest.fixture
def warehouses_object1():
    return [{"warehouse1": {"size": "xsmall"}}, {"warehouse2": {"size": "xsmall"}}]


@pytest.fixture
def warehouses_object2():
    return [{"warehouse3": {"size": "medium"}}, {"warehouse2": {"size": "xsmall"}}]


@pytest.fixture
def warehouses_loaded():
    warehouses = Warehouses_Module()
    warehouses.spesification = {
        "warehouse1": {"size": "xsmall"},
        "warehouse2": {"size": "xsmall"},
        "warehouse3": {"size": "medium"},
    }
    return warehouses


def test_warehouse_module_add_entities(warehouses_object1):
    warehouses = Warehouses_Module()
    warehouses.add_entities(warehouses_object1)
    assert warehouses.spesification == [
        {"warehouse1": {"size": "xsmall"}},
        {"warehouse2": {"size": "xsmall"}},
    ]


def test_warehouse_module_add_entities(
    warehouses_object1, warehouses_object2, warehouses_loaded
):
    warehouses = Warehouses_Module()
    warehouses.add_entities(warehouses_object1)
    warehouses.add_entities(warehouses_object2)
    assert warehouses.spesification == warehouses_loaded.spesification


def test_warehouse_module_get_warehouse(warehouses_loaded):
    assert warehouses_loaded.get_entities("warehouse1") == {"size": "xsmall"}


def test_warehouse_module_get_warehouse_not_found(warehouses_loaded):
    with pytest.raises(Exception) as exception_info:
        warehouses_loaded.get_entities("warehouse4")
    assert exception_info.type == Exception
    assert exception_info.value.args[0] == "Warehouse not found"


def test_warehouse_is_warehouse(warehouses_loaded):
    assert warehouses_loaded.is_entity("warehouse1") == True


def test_warehouse_is_warehouse_not_found(warehouses_loaded):
    assert warehouses_loaded.is_entity("warehouse4") == False


def test_warehouse_describe(warehouses_loaded):
    warehouse_description = warehouses_loaded.describe()
    assert warehouse_description.count == 3
    assert set(warehouse_description.entities) == set(
        ["warehouse1", "warehouse2", "warehouse3"]
    )


def test_warehouse_describe_empty():
    warehouses = Warehouses_Module()
    warehouse_description = warehouses.describe()
    assert warehouse_description.count == 0
    assert set(warehouse_description.entities) == set([])
