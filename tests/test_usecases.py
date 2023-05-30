import pytest
import os
import logging

from src.Spesification import Spesification
from src.Reader import Reader


def yaml_spessification_conctinated(file_path):
    control_spec = Spesification()
    control_spec.load(file_path)
    control_spec.identify_modules()
    control_spec.identify_entities()
    return control_spec.spec_file


def test_simple_generation():
    spec = Spesification()
    spec.load("tests/data/base_premissions/team_a_permisions.yml")
    spec.identify_modules()
    spec.identify_entities()
    spec.generate()
    spec.export("tests/data/generated/team_a_permisions.yml")
    assert spec.generated == True
    assert isinstance(spec.output, str)
    assert spec.output != ""
    assert spec.output == open("tests/data/generated/team_a_permisions.yml").read()
    assert spec.spec_file == yaml_spessification_conctinated(
        "tests/data/generated/team_a_permisions.yml"
    )
    try:
        os.remove("tests/data/generated/team_a_permisions.yml")
    except:
        pass


def test_simple_concatination():
    spec = Spesification()
    spec.load("tests/data/base_premissions/")
    spec.identify_modules()
    spec.identify_entities()
    spec.generate()
    spec.export("tests/data/generated/Concatinated_permissions.yml")
    assert spec.generated == True
    assert isinstance(spec.output, str)
    assert spec.output != ""
    assert (
        spec.output == open("tests/data/generated/Concatinated_permissions.yml").read()
    )
    assert spec.spec_file == yaml_spessification_conctinated(
        "tests/data/generated/Concatinated_permissions.yml"
    )
    try:
        os.remove("tests/data/generated/Concatinated_permissions.yml")
    except:
        pass

def test_appended_concatination_with_verification():
    spec = Spesification(verification=True)
    spec.load("tests/data/verification_error_premissions/")
    spec.identify_modules()
    spec.identify_entities()
    spec.generate()
    spec.export("tests/data/generated/verified_permissions.yml")
    assert spec.verified == True
    assert spec.spec_file == yaml_spessification_conctinated("tests/data/verified_permissions.yml")
    try:
        os.remove("tests/data/generated/verified_permissions.yml")
    except:
        pass

    
