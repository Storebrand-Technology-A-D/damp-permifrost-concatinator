import logging
import os
import pytest

from src.permifrost_concatinator.loader_local_file import Local_file_loader


def test_loader_local_file_json():
    loader = Local_file_loader("json")
    json = loader.load("tests/data/permision_state.json")
    assert isinstance(json, dict)

def test_loader_local_file_yaml():
    loader = Local_file_loader("yaml")
    yaml = loader.load("tests/data/verified_permissions.yml")
    assert isinstance(yaml, dict)