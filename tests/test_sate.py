import pytest
from src.permifrost_concatinator.Permission_state import Permission_state


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
