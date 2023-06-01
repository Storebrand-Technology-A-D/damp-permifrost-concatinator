import pytest
import logging
from src.verification_module import SpecVerification


def test_spec_verification_database_missing_owners(spesification_team_c, caplog):
    caplog.set_level(logging.ERROR)
    spec_verification = SpecVerification(spesification_team_c)
    assert spec_verification.databases() == False
    assert len(caplog.records) == 1

def test_spec_verification_database_all_ok(spesification_team_c_verified, caplog):
    caplog.set_level(logging.ERROR)
    spec_verification = SpecVerification(spesification_team_c_verified)
    assert spec_verification.databases() == True
    assert len(caplog.records) == 0

def test_spec_verification_users_missing_roles(spesification_team_c, caplog):
    caplog.set_level(logging.ERROR)
    spec_verification = SpecVerification(spesification_team_c)
    assert spec_verification.users() == False
    assert len(caplog.records) == 1

def test_spec_verification_users_all_ok(spesification_team_c_verified, caplog):
    caplog.set_level(logging.ERROR)
    spec_verification = SpecVerification(spesification_team_c_verified)
    assert spec_verification.users() == True
    assert len(caplog.records) == 0

def test_spec_verification_warhouses_missing_roles(spesification_team_c, caplog):
    caplog.set_level(logging.ERROR)
    spec_verification = SpecVerification(spesification_team_c)
    assert spec_verification.warehouses() == False
    assert len(caplog.records) == 1

def test_spec_verification_warhouses_all_ok(spesification_team_c_verified, caplog):
    caplog.set_level(logging.ERROR)
    spec_verification = SpecVerification(spesification_team_c_verified)
    assert spec_verification.warehouses() == True
    assert len(caplog.records) == 0

def test_spec_verification_roles_missing_roles(spesification_team_c, caplog):
    caplog.set_level(logging.ERROR)
    spec_verification = SpecVerification(spesification_team_c)
    assert spec_verification.roles() == False
    assert len(caplog.records) == 3

def test_spec_verification_roles_all_ok(spesification_team_c_verified, caplog):
    caplog.set_level(logging.ERROR)
    spec_verification = SpecVerification(spesification_team_c_verified)
    assert spec_verification.roles() == True
    assert len(caplog.records) == 0