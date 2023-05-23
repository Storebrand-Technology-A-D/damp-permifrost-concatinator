import pytest
import os

from src.Spesification import Spesification

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
    try:
        os.remove("tests/data/generated/team_a_permisions.yml")
    except:
        pass

    