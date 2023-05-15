import pytest
from src.Databases import Databases_Module


@pytest.fixture
def databases_object1():
    return [
        {"database1": {"shared": False}},
        {"database2": {"shared": False, "owner": "loader_qlik"}},
    ]


@pytest.fixture
def databases_object2():
    return [
        {"database3": {"shared": True, "owner": "loader_qlik"}},
        {"database2": {"shared": False, "owner": "loader_qlik"}},
    ]


@pytest.fixture
def databases_loaded():
    databases = Databases_Module()
    databases.spesification = {
        "database1": {"shared": False},
        "database2": {"shared": False, "owner": "loader_qlik"},
        "database3": {"shared": True, "owner": "loader_qlik"},
    }
    return databases


def test_database_module_add_entities(databases_object1):
    databases = Databases_Module()
    databases.add_entities(databases_object1)
    assert databases.spesification == {
        "database1": {"shared": False},
        "database2": {"shared": False, "owner": "loader_qlik"},
    }


def test_database_module_add_entities(
    databases_object1, databases_object2, databases_loaded
):
    databases = Databases_Module()
    databases.add_entities(databases_object1)
    databases.add_entities(databases_object2)
    assert databases.spesification == databases_loaded.spesification


def test_database_module_get_database(databases_loaded):
    assert databases_loaded.get_entitiy("database1") == {"shared": False}
    assert databases_loaded.get_entitiy("database2") == {
        "shared": False,
        "owner": "loader_qlik",
    }


def test_database_module_get_database_not_found(databases_loaded):
    with pytest.raises(Exception) as exception_info:
        databases_loaded.get_entitiy("database4")
    assert exception_info.type == Exception
    assert exception_info.value.args[0] == "Database not found"


def test_database_is_database(databases_loaded):
    assert databases_loaded.is_entity("database1") == True


def test_database_is_database_not_found(databases_loaded):
    assert databases_loaded.is_entity("database4") == False


def test_database_describe(databases_loaded):
    databases_description = databases_loaded.describe()
    assert databases_description.count == 3
    assert databases_description.entities == ["database1", "database2", "database3"]


def test_database_describe_empty():
    databases = Databases_Module()
    databases_description = databases.describe()
    assert databases_description.count == 0
    assert databases_description.entities == []
