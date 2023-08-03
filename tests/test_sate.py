import pytest
import os
import json
from src.permifrost_concatinator.Permission_state import Permission_state
from src.permifrost_concatinator.loader_local_file import Local_file_loader


def test_permision_state_exists(spesification_team_c_verified):
    """
    Test that the Permission_state class generates a permission state object
    """
    permission_state = Permission_state(spesification_team_c_verified)
    assert permission_state is not None


def test_permisison_state_generate(
    spesification_team_c_verified, team_c_verefied_state_file
):
    """
    test that permission state generates a state file
    """
    permission_state = Permission_state(spesification_team_c_verified)
    permission_state.generate()
    assert permission_state.state_file is not None
    assert permission_state.state_file.keys() == {
        "version",
        "serial",
        "modules",
        "generated",
    }
    assert permission_state.state_file == team_c_verefied_state_file


def test_permision_state_export(
    spesification_team_c_verified, team_c_verefied_state_file
):
    """
    Test that the Permission_state class exports a permission state file
    """
    permission_state = Permission_state(spesification_team_c_verified)
    permission_state.export("tests/data/generated/permision_state_export.json")
    with open("tests/data/generated/permision_state_export.json", "r") as file:
        output = json.load(file)
    assert output == team_c_verefied_state_file
    try:
        os.remove("tests/data/generated/permision_state_export.json")
    except FileNotFoundError:
        pass


def test_permision_state_load(team_c_verefied_state_file):
    permission_state = Permission_state().load(
        Local_file_loader, "tests/data/permision_state.json"
    )
    assert permission_state.state_file == team_c_verefied_state_file


def test_permision_state_load_not_found():
    with pytest.raises(FileNotFoundError):
        permission_state = Permission_state().load(
            Local_file_loader, "tests/data/permision_state_not_found.json"
        )


def test_permision_state_load_not_json():
    with pytest.raises(json.decoder.JSONDecodeError):
        permission_state = Permission_state().load(
            Local_file_loader, "tests/data/real_permisions.yml"
        )


@pytest.mark.skip(reason="Not implemented")
def test_permission_state_compare(
    spesification_team_c_verified,
    spesification_team_a,
    team_ac_state_create,
    team_ac_state_update,
):
    team_c_state = Permission_state(spesification_team_c_verified).generate()
    team_a_state = Permission_state(spesification_team_a).generate()
    state_diff = team_c_state.compare(team_a_state)

    assert state_diff.create == team_ac_state_create
    assert state_diff.update == team_ac_state_update
