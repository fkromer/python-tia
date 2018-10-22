from tia.config import read

def test_read_config_file(tmpdir):
    cf = tmpdir.mkdir("subdir").join("tia.yaml")
    expected_str = """
    some
    multi
    line
    config
    """
    cf.write(expected_str)
    file_path = str(cf)
    assert read(file_path) == expected_str
