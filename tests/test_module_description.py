import pytest
from src.permifrost_concatinator.Module_description import Module_description
from src.permifrost_concatinator.Databases_module import Databases_Module


def test_module_description_gather_description(databases_object):
    description = Module_description("databases")
    description.gather_description(databases_object)
    assert description.count == 3
    assert description.entities == ["database1", "database2", "database3"]


def test_module_description_return_description(databases_object):
    description = Module_description("databases")
    description.gather_description(databases_object)
    assert description.return_description() == {
        "count": 3,
        "entities": ["database1", "database2", "database3"],
    }
