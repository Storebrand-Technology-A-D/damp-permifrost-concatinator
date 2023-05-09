import pytest
from src.Reader import Reader

def test_reader_read_dir():
    reader = Reader()
    assert reader.read_dir('tests/data') == ['tests/data/team_a_permisions.yml', 'tests/data/team_b_permisions.yml']
    assert reader.files == ['tests/data/team_a_permisions.yml', 'tests/data/team_b_permisions.yml']

def test_reader_read_dir_empty():
    reader = Reader()
    assert reader.read_dir('tests/data/empty') == []
    assert reader.files == []


