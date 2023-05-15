import pytest
from src.Module_description import Module_description
from src.Databases import Databases_Module


@pytest.fixture
def databases():
    database = Databases_Module()
    database.spesification = {
        "database1": {"shared": False},
        "database2": {"shared": False, "owner": "loader_qlik"},
    }
    return database


def test_module_description_gather_description(databases):
    description = Module_description("databases")
    description.gather_description(databases)
    assert description.count == 2
    assert description.entities == ["database1", "database2"]


def test_module_description_return_description(databases):
    description = Module_description("databases")
    description.gather_description(databases)
    assert description.return_description() == {
        "count": 2,
        "entities": ["database1", "database2"],
    }
