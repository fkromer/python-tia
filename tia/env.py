# CI environment detection via corresponding ENV vars at time of writing (31. October 2018)
#
# Not considered yet:
# - Buildbot: https://buildbot.net/
# - CumulusCI: https://github.com/SFDO-Tooling/CumulusCI

from os import getenv


def is_ci() -> bool:
    #pylint: disable=simplifiable-if-statement, too-many-boolean-expressions
    if (_is_appveyor_ci() or _is_azure_ci() or _is_circle_ci() or _is_drone_ci() or _is_gitlab_ci()
            or _is_jenkins_ci() or _is_scrutinizer_ci() or _is_semaphore_ci() or _is_shippable_ci()
            or _is_travis_ci()):
        return True
    else:
        return False


def _is_appveyor_ci() -> bool:
    # APPVEYOR=True, CI=True (both true on Ubuntu image)
    # https://www.appveyor.com/docs/environment-variables/
    ci_env_var: str = 'APPVEYOR'
    return _is_env_set(ci_env_var)


def _is_azure_ci() -> bool:
    # TF_BUILD=True
    # https://docs.microsoft.com/en-us/azure/devops/pipelines/build/variables?view=vsts#system-variables
    ci_env_var: str = 'TF_BUILD'
    return _is_env_set(ci_env_var)


def _is_circle_ci() -> bool:
    # CIRCLECI=true, CI=true
    # https://circleci.com/docs/2.0/env-vars/#built-in-environment-variables
    ci_env_var: str = 'CIRCLE_CI'
    return _is_env_set(ci_env_var)


def _is_drone_ci() -> bool:
    # DRONE=true, CI=drone
    # http://docs.drone.io/environment-reference/
    ci_env_var: str = 'DRONE'
    return _is_env_set(ci_env_var)


def _is_gitlab_ci() -> bool:
    # GITLAB_CI=true, CI=true
    # https://docs.gitlab.com/ee/ci/variables/#predefined-variables-environment-variables
    ci_env_var: str = 'GITLAB_CI'
    return _is_env_set(ci_env_var)


def _is_jenkins_ci() -> bool:
    # JENKINS_URL (no CI env var)
    # https://wiki.jenkins.io/display/JENKINS/Building+a+software+project#Buildingasoftwareproject-belowJenkinsSetEnvironmentVariables
    ci_env_var: str = 'JENKINS_URL'
    return _is_env_set(ci_env_var)


def _is_scrutinizer_ci() -> bool:
    # SCRUTINIZER=true, CI=true
    # https://scrutinizer-ci.com/docs/build/environment-variables#pre-defined-environment-variables
    ci_env_var: str = 'SCRUTINIZER'
    return _is_env_set(ci_env_var)


def _is_semaphore_ci() -> bool:
    # SEMAPHORE=true, CI=true
    # https://semaphoreci.com/docs/available-environment-variables.html#variables-exported-in-builds-and-deploys
    ci_env_var: str = 'SEMAPHORE'
    return _is_env_set(ci_env_var)


def _is_shippable_ci() -> bool:
    # SHIPPABLE=true, CI=true
    # http://docs.shippable.com/ci/env-vars/#stdEnv
    ci_env_var: str = 'SHIPPABLE'
    return _is_env_set(ci_env_var)


def _is_travis_ci() -> bool:
    # TRAVIS=true, CI=true
    # https://docs.travis-ci.com/user/environment-variables/#default-environment-variables
    ci_env_var: str = 'TRAVIS'
    return _is_env_set(ci_env_var)


def _is_env_set(env_var: str) -> bool:
    if getenv(env_var, default=None) is not None:
        return True
    else:
        return False
