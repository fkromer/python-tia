from tia.env import is_ci

def test_is_some_ci(monkeypatch):
    monkeypatch.setenv('CIRCLE_CI', '')
    monkeypatch.setenv('GITLAB_CI', '')
    monkeypatch.setenv('JENKINS_URL', '')
    monkeypatch.setenv('TRAVIS', '')
    assert is_ci()

def test_is_no_ci():
    # implicitly unset ci env vars
    assert not is_ci()
