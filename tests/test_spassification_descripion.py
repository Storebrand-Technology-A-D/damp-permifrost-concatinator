import pytest
from src.Spesification_description import Spessification_description


def test_spesification_description_load_module_description(warehouses_description):
    description = Spessification_description()
    description.load_module_description("warehouses", warehouses_description)
    assert description.warehouses != None
    assert description.warehouses.keys() == {"count", "entities"}
