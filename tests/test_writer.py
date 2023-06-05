import pytest
import os.path
from src.permifrost_concatinator.Reader import Reader
from src.permifrost_concatinator.Writer_yaml_file import Yaml_file_Writer


def test_yaml_file_Writer_file_exists():
    writer = Yaml_file_Writer()
    writer.write("test1.yml", "test")
    assert os.path.isfile("test1.yml") == True
    try:
        os.remove("test1.yml")
    except:
        pass


def test_yaml_file_Writer_file_content():
    writer = Yaml_file_Writer()
    writer.write("test2.yml", "test")
    with open("test2.yml", "r") as file:
        content = file.read()
    assert content == "test"
    try:
        os.remove("test2.yml")
    except:
        pass


def test_yaml_file_Writer_formatting(
    databases_object_str_results, warehouses_object_str_results
):
    spec_output = (
        f"""version: "0.14.0"\n"""
        + databases_object_str_results
        + warehouses_object_str_results
    )
    writer = Yaml_file_Writer()
    writer.write("test3.yml", spec_output)
    with open("test3.yml", "r") as file:
        content = file.read()
    assert content == spec_output
    try:
        os.remove("test3.yml")
    except:
        pass


def test_yaml_file_Writer_file_is_yaml(
    warehouses_object_str_results,
    roles_object_str_results,
):
    spec_output = (
        f"""version: "0.14.0"\n"""
        + warehouses_object_str_results
        + roles_object_str_results
    )
    writer = Yaml_file_Writer()
    writer.write("test4.yml", spec_output)

    reader = Reader()
    test_file = reader.get_file("test4.yml")

    assert test_file != None
    try:
        os.remove("test4.yml")
    except:
        pass
