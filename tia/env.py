# CI environmen detection considers CIs CircleCi, GitLab CI, Jenkins, Travis
# with corresponding ENV vars at time of writing (27. October 2018)

from os import getenv

def is_ci() -> bool:
    if (_is_circle_ci() or _is_gitlab_ci() or _is_jenkins_ci() or _is_travis_ci()):  #pylint: disable=simplifiable-if-statement
        return True
    else:
        return False

def _is_circle_ci() -> bool:
    ci_env_var: str = 'CIRCLE_CI'
    return _is_env_set(ci_env_var)

def _is_gitlab_ci() -> bool:
    ci_env_var: str = 'GITLAB_CI'
    return _is_env_set(ci_env_var)

def _is_jenkins_ci() -> bool:
    ci_env_var: str = 'JENKINS_URL'
    return _is_env_set(ci_env_var)

def _is_travis_ci() -> bool:
    ci_env_var: str = 'TRAVIS'
    return _is_env_set(ci_env_var)

def _is_env_set(ci: str) -> bool:
    if getenv(ci, default=None) != None:
        return True
    else:
        return False
