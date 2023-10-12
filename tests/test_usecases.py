import pytest
import os
import logging

from src.permifrost_concatinator.Spesification import Spesification
from src.permifrost_concatinator.Reader import Reader
from src.permifrost_concatinator.Permission_state import Permission_state
from src.permifrost_concatinator.loader_local_file import Local_file_loader


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


def test_spec_verification_with_error(caplog):
    caplog.set_level(logging.ERROR)
    with pytest.raises(Exception) as exception_info:
        spec = Spesification(verification=True)
        spec.load("tests/data/verification_error_premissions/team_c_permissions.yml")
        spec.identify_modules()
        spec.identify_entities()
        spec.generate()
        spec.export("tests/data/generated/verified_permissions.yml")
        assert exception_info.value.args[0] == "Spec verification failed"
    assert spec.verified == False
    assert len(caplog.records) == 7


def test_spec_verification_pass():
    spec = Spesification(verification=True)
    spec.load("tests/data/verified_permissions.yml")
    spec.identify_modules()
    spec.identify_entities()
    spec.generate()
    spec.export("tests/data/generated/verified_permissions.yml")
    assert spec.verified == True
    assert spec.spec_file == yaml_spessification_conctinated(
        "tests/data/verified_permissions.yml"
    )
    try:
        os.remove("tests/data/generated/verified_permissions.yml")
    except:
        pass


def test_appended_concatination_with_role_generation(caplog):
    caplog.set_level(logging.ERROR)
    spec = Spesification(verification=True, generate_roles=True)
    spec.load("tests/data/permissions_without_ar.yml")
    spec.identify_modules()
    spec.identify_entities()
    spec.generate()
    spec.export("tests/data/generated/imputed_permissions.yml")

    assert yaml_spessification_conctinated(
        "tests/data/generated/imputed_permissions.yml"
    ) == yaml_spessification_conctinated("tests/data/verified_permissions.yml")
    try:
        os.remove("tests/data/generated/imputed_permissions.yml")
    except:
        pass


def test_concatination_plan(caplog, capsys):
    caplog.set_level(logging.INFO)
    spec = Spesification(verification=True, generate_roles=True)
    spec.load("tests/data/permission_teams_without_ar")
    spec.identify_modules()
    spec.identify_entities()
    spec.generate()
    previous_state = Permission_state().load(
        Local_file_loader, "tests/data/permision_state.json"
    )
    current_state = Permission_state(spec).generate()
    current_state.compare(previous_state)
    current_state.plan("")
    captured = capsys.readouterr()
    assert spec.verified == True
    assert captured.out == open("tests/data/plan.txt").read()


def test_state_file_update(caplog, capsys):
    caplog.set_level(logging.INFO)
    spec = Spesification(verification=True, generate_roles=True)
    spec.load("tests/data/permission_teams_without_ar")
    spec.identify_modules()
    spec.identify_entities()
    spec.generate()
    current_state = Permission_state(spec).generate()
    current_state.export("tests/data/generated/permision_state.json")
    updated_state = Permission_state().load(
        Local_file_loader, "tests/data/generated/permision_state.json"
    )
    updated_state.compare(current_state)
    updated_state.plan("")
    captured = capsys.readouterr()
    assert current_state.serial < updated_state.serial
    assert captured.out == open("tests/data/no_change_plan.txt").read()
    try:
        os.remove("tests/data/generated/permision_state.json")
    except:
        pass


@pytest.mark.skip(reason="only for timning purposes")
def test_spec_verification_real(caplog):
    caplog.set_level(logging.INFO)
    spec = Spesification(verification=True)
    spec.load("tests/data/real_permisions.yml")
    spec.identify_modules()
    spec.identify_entities()
    spec.generate()
    assert spec.verified == True
