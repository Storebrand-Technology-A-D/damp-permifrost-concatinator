import pytest
import yaml

from src.Spesification import Spesification


def load_yaml(yaml_file):
    with open(yaml_file, "r") as in_fh:
        file = yaml.safe_load(in_fh)
    return file


@pytest.fixture
def real_spesification_object():
    return load_yaml("tests/data/real_permisions.yml")


@pytest.fixture
def real_spesification_loaded():
    spec = Spesification()
    spec.spec_file = load_yaml("tests/data/real_permisions.yml")
    return spec


@pytest.fixture
def spesification_object():
    return load_yaml("tests/data/base_premissions/team_a_permisions.yml")


@pytest.fixture
def spesification_onject2():
    return load_yaml("tests/data/base_premissions/team_b_permisions.yml")


@pytest.fixture
def spesification_loaded():
    spec = Spesification()
    spec.spec_file = load_yaml("tests/data/base_premissions/team_a_permisions.yml")
    return spec


@pytest.fixture
def spesification_loaded2():
    spec = Spesification()
    spec.spec_file = load_yaml("tests/data/base_premissions/team_b_permisions.yml")
    return spec


def test_spessification_load_spec(spesification_object):
    spesification = Spesification()
    spesification.load(spesification_object)
    assert spesification.spec_file == spesification_object


def test_spesification_module_identify(spesification_loaded):
    spesification_loaded.identify_modules()
    assert set(spesification_loaded.module_list) == set(
        ["roles", "users", "warehouses", "databases"]
    )


def test_spesification_identify_entities(spesification_loaded):
    spesification_loaded.identify_modules()
    load_confirmation = spesification_loaded.identify_entities()
    assert load_confirmation == True


def test_spesification_describe(spesification_loaded):
    spesification_loaded.identify_modules()
    spesification_loaded.identify_entities()
    description = spesification_loaded.describe()
    assert description.databases.keys() == {"count", "entities"}
    assert description.roles.keys() == {"count", "entities"}
    assert description.users.keys() == {"count", "entities"}


# def test_spesification_append_spec(spesification_loaded, spesification_onject2):
#    spesification_loaded.append_spec(spesification_onject2)
