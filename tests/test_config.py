from tia.config import read_file
from pytest import raises

def test_reading_existing_config_file_returns_string(tmpdir):
    cf = tmpdir.mkdir("subdir").join("tia.yaml")
    expected_str = """
    some
    multi
    line
    config
    """
    cf.write(expected_str)
    file_path = str(cf)
    assert read_file(file_path) == expected_str

def test_reading_non_existing_config_file_raises_exception():
    file_path = "/nonexisting"
    expected_str = "irrelevant"
    with raises(Exception):
        assert read_file(file_path) == expected_str
