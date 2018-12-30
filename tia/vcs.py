"""
Functionality to access git version control system information.

TODO: add unit tests
"""

from git import Repo

from typing import Iterator

ChangedFile = str
ChangedFiles = Iterator[ChangedFile]


def get_repo(path="."):
    repo = Repo(path)
    return repo


def get_untracked_files(repo: Repo) -> ChangedFiles:
    """
    In case of non CI environment untracked files are considered changed w.r.t.
    need for tia pipeline execution.
    """
    for f in repo.untracked_files:
        yield f


def get_changed_staged_files(repo: Repo) -> ChangedFiles:
    """
    Yields paths of staged files which have been added, modified or renamed.
    Files which have been modified and renamed are yielded only once.
    """
    hcommit = repo.head.commit
    changes = hcommit.diff()
    # TODO: improve performance and get rid of mutable set
    files = set()
    for f in changes.iter_change_type('A'):
        files.add(f.b_path)
    for f in changes.iter_change_type('M'):
        files.add(f.b_path)
    for f in changes.iter_change_type('R'):
        files.add(f.b_path)
    for f in files:
        yield f
    del files  # free memory from set


def get_changed_unstaged_files(repo: Repo) -> ChangedFiles:
    """
    Yields paths of unstaged files (versioned files in working tree)
    which have been modified or renamed.
    Files which have been modified and renamed are yielded only once.
    """
    changes = repo.index.diff(None)
    # TODO: improve performance and get rid of mutable set
    files = set()
    for f in changes.iter_change_type('M'):
        files.add(f.b_path)
    for f in changes.iter_change_type('R'):
        files.add(f.b_path)
    for f in files:
        yield f
    del files  # free memory from set


def get_changed_files_non_ci(repo: Repo) -> ChangedFiles:
    """
    File changes considered for tia invocation not in CI are unstaged and
    staged file changes.
    """
    unstaged_files = changed_unstaged_files(repo)
    staged_files = changed_staged_files(repo)
    yield from unstaged_files
    yield from staged_files


def get_changed_files_ci(repo: Repo) -> ChangedFiles:
    """
    File changes considered for tia invocation in CI are changed files between
    the current HEAD and the last commit.
    Yields paths of new, modified and renamed files.
    Files which have been modified and renamed are yielded only once.
    """
    hcommit = repo.head.commit
    changes = hcommit.diff('HEAD~1')
    # TODO: improve performance and get rid of mutable set
    files = set()
    for f in changes.iter_change_type('A'):
        files.add(f.b_path)
    for f in changes.iter_change_type('M'):
        files.add(f.b_path)
    for f in changes.iter_change_type('R'):
        files.add(f.b_path)
    for f in files:
        yield f
    del files  # free memory from set
