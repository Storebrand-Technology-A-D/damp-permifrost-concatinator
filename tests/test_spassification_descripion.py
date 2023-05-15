import pytest
from src.Spesification_description import Spessification_description
from src.Databases import Databases_Module
from src.Warehouses import Warehouses_Module


@pytest.fixture
def databases():
    database = Databases_Module()
    database.spesification = {
        "database1": {"shared": False},
        "database2": {"shared": False, "owner": "loader_qlik"},}
    return database.describe()

@pytest.fixture
def warehouses():
    warehouse = Warehouses_Module()
    warehouse.spesification = {
        "warehouse1": {"size": "xsmall"},
        "warehouse2": {"size": "xsmall"},
        "warehouse3": {"size": "medium"},
    }
    return warehouse.describe()

def test_spesification_description_load_module_description(warehouses):
    description = Spessification_description()
    description.load_module_description("warehouses", warehouses)
    assert description.warehouses != None
    assert description.warehouses.keys() == {"count", "entities"}