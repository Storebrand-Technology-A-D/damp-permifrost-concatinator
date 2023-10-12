import yaml
import pytest
from src.permifrost_concatinator.Reader import Reader


def load_yaml(yaml_file):
    with open(yaml_file, "r") as in_fh:
        file = yaml.safe_load(in_fh)
    return file


def test_reader_read_dir():
    reader = Reader()
    assert set(reader.read_dir("tests/data/base_premissions")) == set(
        [
            "tests/data/base_premissions/team_a_permisions.yml",
            "tests/data/base_premissions/team_b_permisions.yml",
        ]
    )
    assert set(reader.files) == set(
        [
            "tests/data/base_premissions/team_a_permisions.yml",
            "tests/data/base_premissions/team_b_permisions.yml",
        ]
    )


def test_reader_read_dir_empty():
    reader = Reader()
    with pytest.raises(Exception) as exception_info:
        assert reader.read_dir("tests/data/empty") == []
        assert exception_info.type == FileNotFoundError
        assert exception_info.value.args[0] == "Directory not found"
        assert reader.files == []


def test_reader_read_dir_not_found():
    reader = Reader()
    with pytest.raises(Exception):
        reader.read_dir("tests/data/not_found")
    assert reader.files == []


def test_reader_read_dir_not_dir():
    reader = Reader()
    with pytest.raises(Exception):
        reader.read_dir("tests/data/base_premissions/team_a_permisions.yml")
    assert reader.files == []


def test_reader_get_file():
    reader = Reader()
    files_list = [
        "tests/data/base_premissions/team_a_permisions.yml",
        "tests/data/base_premissions/team_b_permisions.yml",
    ]
    reader.files = files_list
    file1 = reader.get_file(files_list[0])
    assert file1 == load_yaml(files_list[0])


def test_reader_get_file_not_found():
    reader = Reader()
    with pytest.raises(Exception) as exception_info:
        reader.get_file("tests/data/not_found.yml")
    assert exception_info.type == Exception
    assert exception_info.value.args[0] == "File not found"


def test_reader_get_file_not_yaml():
    reader = Reader()
    with pytest.raises(Exception) as exception_info:
        reader.get_file("tests/data/errors/permissions.txt")
    assert exception_info.type == Exception
    assert exception_info.value.args[0] == "File not yaml"


def test_reader_get_file_not_file():
    reader = Reader()
    with pytest.raises(Exception) as exception_info:
        reader.get_file("tests/data/base_premissions")
    assert exception_info.type == IsADirectoryError


def test_reader_get_file_empty():
    reader = Reader()
    with pytest.raises(Exception) as exception_info:
        reader.get_file("tests/data/empty/empty.yml")
    assert exception_info.type == Exception
    assert exception_info.value.args[0] == "File not found"
