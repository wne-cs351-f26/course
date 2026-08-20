"""Tests for the begin and save commands.

Each test builds a throwaway student repository and a throwaway course
repository, then runs the real scripts against them via subprocess.
"""

import os
import subprocess
import pytest

BIN = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "bin")


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo)] + list(args),
                          capture_output=True, text=True)


def init_repo(path):
    path.mkdir(parents=True, exist_ok=True)
    git(path, "init", "-q", "-b", "main")
    git(path, "config", "user.email", "t@t.t")
    git(path, "config", "user.name", "t")
    (path / "README.md").write_text("student repo\n")
    git(path, "add", "-A")
    git(path, "commit", "-q", "-m", "init")
    return path


@pytest.fixture
def course(tmp_path):
    c = init_repo(tmp_path / "course")
    src = c / "src" / "a1"
    src.mkdir(parents=True)
    (src / "grammar").write_text("token ID '\\w+'\n")
    (src / "README.md").write_text("assignment 1\n")
    git(c, "add", "-A")
    git(c, "commit", "-q", "-m", "add a1")
    return c


@pytest.fixture
def student(tmp_path):
    return init_repo(tmp_path / "student")


def run_begin(student, course, *args):
    env = dict(os.environ,
               CS351_REPO_ROOT=str(student),
               CS351_COURSE=str(course))
    return subprocess.run([os.path.join(BIN, "begin")] + list(args),
                          capture_output=True, text=True, env=env, cwd=str(student))


def test_begin_copies_assignment_files(student, course):
    r = run_begin(student, course, "a1")
    assert r.returncode == 0, r.stderr
    assert (student / "a1" / "grammar").exists()


def test_begin_records_pristine_copy(student, course):
    run_begin(student, course, "a1")
    pristine = student / ".cs351" / "pristine" / "a1" / "grammar"
    assert pristine.exists()
    assert pristine.read_text() == (course / "src" / "a1" / "grammar").read_text()


def test_begin_commits_only_the_assignment(student, course):
    (student / "myfile.txt").write_text("student work\n")
    git(student, "add", "myfile.txt")
    run_begin(student, course, "a1")
    files = git(student, "show", "--name-only", "--format=", "HEAD").stdout.split()
    assert "a1/grammar" in files
    assert "myfile.txt" not in files
    staged = git(student, "diff", "--cached", "--name-only").stdout.split()
    assert "myfile.txt" in staged


def test_begin_refuses_unknown_assignment(student, course):
    r = run_begin(student, course, "nope")
    assert r.returncode != 0
    assert "No such assignment" in r.stderr


def test_begin_refuses_existing_without_force(student, course):
    run_begin(student, course, "a1")
    r = run_begin(student, course, "a1")
    assert r.returncode != 0
    assert "already exists" in r.stderr


def test_begin_overwrites_with_force(student, course):
    run_begin(student, course, "a1")
    (student / "a1" / "grammar").write_text("student edited\n")
    r = run_begin(student, course, "-f", "a1")
    assert r.returncode == 0, r.stderr
    assert (student / "a1" / "grammar").read_text() == "token ID '\\w+'\n"


def test_begin_refuses_conflicted_repo_before_copying(student, course):
    # Manufacture an unresolved merge conflict.
    (student / "shared.txt").write_text("base\n")
    git(student, "add", "-A"); git(student, "commit", "-q", "-m", "base")
    git(student, "checkout", "-qb", "other")
    (student / "shared.txt").write_text("theirs\n")
    git(student, "commit", "-qam", "theirs")
    git(student, "checkout", "-q", "main")
    (student / "shared.txt").write_text("mine\n")
    git(student, "commit", "-qam", "mine")
    git(student, "merge", "other")

    r = run_begin(student, course, "a1")
    assert r.returncode != 0
    assert "unfinished merge" in r.stderr
    # Critical: it must refuse BEFORE copying, so nothing is half-applied.
    assert not (student / "a1").exists()


def test_begin_lists_assignments_with_no_arguments(student, course):
    r = run_begin(student, course)
    assert "a1" in r.stderr


def test_save_commits_in_repo_root_not_cwd(student, course, tmp_path):
    """save must act on CS351_REPO_ROOT even when run from a nested repo."""
    nested = init_repo(student / "tmp" / "nested")
    (student / "work.txt").write_text("my work\n")

    env = dict(os.environ, CS351_REPO_ROOT=str(student))
    r = subprocess.run([os.path.join(BIN, "save"), "my message"],
                       capture_output=True, text=True, env=env, cwd=str(nested))

    # push fails (no remote); commit must still have landed in the student repo.
    log = git(student, "log", "--oneline", "-1").stdout
    assert "my message" in log
    nested_log = git(nested, "log", "--oneline", "-1").stdout
    assert "my message" not in nested_log
