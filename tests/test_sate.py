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
    assert permission_state.state is not None
    assert permission_state.state.keys() == {
        "version",
        "serial",
        "modules",
        "generated",
    }
    assert permission_state.state == team_c_verefied_state_file


def test_permision_state_export(
    spesification_team_c_verified, team_c_verefied_state_file
):
    """
    Test that the Permission_state class exports a permission state file
    """
    working_dir = os.getcwd()
    permission_state = Permission_state(spesification_team_c_verified)
    permission_state.export(f"{working_dir}/tests/data/generated/permision_state_export.json")
    with open(f"{working_dir}/tests/data/generated/permision_state_export.json", "r") as file:
        output = json.load(file)
    assert output == team_c_verefied_state_file
    try:
        os.remove(f"{working_dir}/tests/data/generated/permision_state_export.json")
    except FileNotFoundError:
        pass


def test_permision_state_load(team_c_verefied_state_file):
    permission_state = Permission_state().load(
        Local_file_loader, "tests/data/permision_state.json"
    )
    assert permission_state.state == team_c_verefied_state_file


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


def test_permission_state_compare(
    spesification_team_c_verified,
    spesification_team_a,
    team_ac_state_update,
    team_ca_state_update,
    caplog,
):
    caplog.set_level("DEBUG")
    team_c_state = Permission_state(spesification_team_c_verified).generate()
    team_a_state = Permission_state(spesification_team_a).generate()
    ac_state_diff = team_c_state.compare(team_a_state)

    assert set(ac_state_diff.state_changes) == team_ac_state_update
    ca_state_diff = team_a_state.compare(team_c_state)
    assert set(ca_state_diff.state_changes) == team_ca_state_update


def test_permission_state_plan_create(
    spesification_team_c_verified, spesification_team_a, team_ca_plan, capsys, caplog
):
    caplog.set_level("DEBUG")
    team_c_state = Permission_state(spesification_team_c_verified).generate()
    team_a_state = Permission_state(spesification_team_a).generate()
    team_c_state.compare(team_a_state)
    team_c_state.plan("")
    captured = capsys.readouterr()
    assert captured.out == team_ca_plan


def test_permission_state_plan_delete(
    spesification_team_c_verified, spesification_team_a, team_ac_plan, capsys, caplog
):
    caplog.set_level("DEBUG")
    team_c_state = Permission_state(spesification_team_c_verified).generate()
    team_a_state = Permission_state(spesification_team_a).generate()
    team_a_state.compare(team_c_state)
    team_a_state.plan("")
    captured = capsys.readouterr()
    assert captured.out == team_ac_plan
