import pytest
import yaml

from src.Spesification import Spesification


def load_yaml(yaml_file):
    with open(yaml_file, "r") as in_fh:
        file = yaml.safe_load(in_fh)
    return file


def test_spesification_module_identify():
    spesification = Spesification(
        load_yaml("tests/data/base_premissions/team_a_permisions.yml")
    )
    spesification.identify()
    assert set(spesification.module_list) == set(
        ["roles", "users", "warehouses", "databases"]
    )
