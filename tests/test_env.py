from tia.env import is_ci
from pytest import mark

@mark.parametrize("ci_env_var", [
    'APPVEYOR',
    'CIRCLE_CI',
    'DRONE',
    'GITLAB_CI',
    'JENKINS_URL',
    'SCRUTINIZER',
    'SEMAPHORE',
    'SHIPPABLE',
    'TRAVIS',
    'TF_BUILD',
])
def test_is_some_ci(monkeypatch, ci_env_var):
    monkeypatch.setenv(ci_env_var, '')
    assert is_ci()

def test_is_no_ci():
    # implicitly unset ci env vars
    assert not is_ci()
