"""Tests for the begin and save commands.

Each test builds a throwaway student repository and a throwaway course
repository, then runs the real scripts against them via subprocess.
"""

import os
import shutil
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
    """A course repo with a1 released and a2 present but NOT released."""
    c = init_repo(tmp_path / "course")
    src = c / "src" / "a1"
    src.mkdir(parents=True)
    (src / "grammar").write_text("token ID '\\w+'\n")
    (src / "README.md").write_text("assignment 1\n")

    unreleased = c / "src" / "a2"
    unreleased.mkdir(parents=True)
    (unreleased / "grammar").write_text("token ID 'draft'\n")

    (c / "released.txt").write_text(
        "# comment line\n"
        "\n"
        "a1\n"
    )
    git(c, "add", "-A")
    git(c, "commit", "-q", "-m", "add a1, draft a2, release a1")
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


def run_save(repo, *args):
    env = dict(os.environ, CS351_REPO_ROOT=str(repo))
    return subprocess.run([os.path.join(BIN, "save")] + list(args),
                          capture_output=True, text=True, env=env, cwd=str(repo))


def test_save_refuses_when_repo_already_conflicted(student, course):
    """Direct check of the new pre-flight guard, mirroring begin's own test."""
    (student / "shared.txt").write_text("base\n")
    git(student, "add", "-A"); git(student, "commit", "-q", "-m", "base")
    git(student, "checkout", "-qb", "other")
    (student / "shared.txt").write_text("theirs\n")
    git(student, "commit", "-qam", "theirs")
    git(student, "checkout", "-q", "main")
    (student / "shared.txt").write_text("mine\n")
    git(student, "commit", "-qam", "mine")
    git(student, "merge", "other")

    before = git(student, "rev-parse", "HEAD").stdout.strip()

    r = run_save(student, "retry")

    assert r.returncode != 0
    assert "again" in r.stderr.lower()
    # Nothing was committed or resolved -- save must not have touched the
    # merge state at all (the conflicted path already shows up in `git
    # diff --cached` as an inherent artifact of an in-progress merge, so
    # that is not itself evidence of anything save did).
    after = git(student, "rev-parse", "HEAD").stdout.strip()
    assert after == before
    assert "<<<<<<<" in (student / "shared.txt").read_text()
    unmerged = git(student, "ls-files", "-u").stdout
    assert "shared.txt" in unmerged


def test_save_does_not_push_conflict_markers_on_retry(student, tmp_path):
    """End-to-end reproduction of the reported failure:

    1. The remote diverges (another codespace / the instructor pushes).
    2. save's own `git pull --no-rebase` conflicts; save must fail without
       pushing.
    3. On retry, save must refuse -- not stage the conflict markers as a
       resolved commit and push them.
    """
    bare = tmp_path / "remote.git"
    subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(bare)],
                   check=True)

    (student / "shared.txt").write_text("base\n")
    git(student, "add", "-A")
    git(student, "commit", "-q", "-m", "base")
    git(student, "remote", "add", "origin", str(bare))
    push = git(student, "push", "-q", "-u", "origin", "main")
    assert push.returncode == 0, push.stderr

    other = tmp_path / "other"
    clone = subprocess.run(["git", "clone", "-q", str(bare), str(other)],
                           capture_output=True, text=True)
    assert clone.returncode == 0, clone.stderr
    git(other, "config", "user.email", "o@o.o")
    git(other, "config", "user.name", "o")
    (other / "shared.txt").write_text("instructor version\n")
    git(other, "commit", "-qam", "instructor edit")
    other_push = git(other, "push", "-q")
    assert other_push.returncode == 0, other_push.stderr

    # The student edits the same file locally without ever pulling.
    (student / "shared.txt").write_text("student version\n")

    first = run_save(student, "attempt1")
    assert first.returncode != 0

    remote_log_after_first = git(bare, "log", "--oneline", "-1", "main").stdout
    assert "instructor edit" in remote_log_after_first
    assert "attempt1" not in remote_log_after_first

    head_after_first = git(student, "rev-parse", "HEAD").stdout.strip()

    # The reflex under deadline pressure: run save again.
    second = run_save(student, "attempt2")
    assert second.returncode != 0
    assert "again" in second.stderr.lower()

    # Nothing new was committed or pushed, and the file on disk still shows
    # unresolved conflict markers rather than a silently "resolved" version.
    head_after_second = git(student, "rev-parse", "HEAD").stdout.strip()
    assert head_after_second == head_after_first

    remote_log_after_second = git(bare, "log", "--oneline", "-1", "main").stdout
    assert "instructor edit" in remote_log_after_second
    assert "attempt2" not in remote_log_after_second

    assert "<<<<<<<" in (student / "shared.txt").read_text()


def test_begin_refuses_an_unreleased_assignment(student, course):
    """a2 exists in src/ but is not in released.txt.

    An unreleased assignment may still change before it is assigned. Because
    begin copies files rather than tracking them, a student who started early
    would be working against a moving target with no way to be notified.
    """
    r = run_begin(student, course, "a2")
    assert r.returncode != 0
    assert "has not been released yet" in r.stderr
    assert not (student / "a2").exists()
    assert not (student / ".cs351" / "pristine" / "a2").exists()


def test_begin_lists_only_released_assignments(student, course):
    r = run_begin(student, course)
    assert "a1" in r.stderr
    assert "a2" not in r.stderr


def test_released_manifest_ignores_comments_and_blank_lines(student, course):
    """The fixture's released.txt carries a comment and a blank line."""
    r = run_begin(student, course, "a1")
    assert r.returncode == 0, r.stderr
    assert (student / "a1" / "grammar").exists()


@pytest.fixture
def course_with_upstream(tmp_path):
    """A course repo cloned from an upstream, so that pulling does something.

    The `course` fixture has no remote, which is fine for everything that only
    reads what is already on disk -- but it cannot show whether begin refreshes.
    """
    upstream = init_repo(tmp_path / "upstream")
    src = upstream / "src" / "a1"
    src.mkdir(parents=True)
    (src / "README.md").write_text("assignment 1\n")
    (upstream / "released.txt").write_text("# nothing released yet\n")
    git(upstream, "add", "-A")
    git(upstream, "commit", "-q", "-m", "a1 present, nothing released")

    clone = tmp_path / "course"
    subprocess.run(["git", "clone", "-q", str(upstream), str(clone)], check=True)
    return upstream, clone


def test_begin_listing_refreshes_course_materials(student, course_with_upstream):
    """Releasing an assignment must reach a student who only runs `begin`.

    released.txt promises that adding a line and pushing takes effect the next
    time any student runs begin, with no action needed from students. That has
    to hold on the listing path too: a student runs `begin` with no arguments
    to find out what is available, so a stale clone there makes a freshly
    released assignment invisible to the person looking for it.
    """
    upstream, course = course_with_upstream

    r = run_begin(student, course)
    assert "a1" not in r.stderr

    (upstream / "released.txt").write_text("a1\n")
    git(upstream, "add", "-A")
    git(upstream, "commit", "-q", "-m", "release a1")

    r = run_begin(student, course)
    assert "a1" in r.stderr


def test_begin_force_replaces_rather_than_merges(student, course):
    """A restructured assignment must not leave the old version's files behind.

    `cp -R` into an existing directory merges. When a1 was rebuilt from six
    questions to three, a student who ran `begin -f` kept the old question
    directories alongside the new ones, while .cs351/pristine held only the new
    files -- so the working copy and the baseline disagreed about what the
    assignment was.
    """
    stale = course / "src" / "a1" / "q_old"
    stale.mkdir()
    (stale / "starter").write_text("old\n")
    git(course, "add", "-A")
    git(course, "commit", "-q", "-m", "a1 with q_old")

    r = run_begin(student, course, "a1")
    assert r.returncode == 0, r.stderr
    assert (student / "a1" / "q_old" / "starter").exists()

    shutil.rmtree(stale)
    git(course, "add", "-A")
    git(course, "commit", "-q", "-m", "restructure a1: drop q_old")

    r = run_begin(student, course, "-f", "a1")
    assert r.returncode == 0, r.stderr
    assert not (student / "a1" / "q_old").exists()
    assert (student / "a1" / "README.md").exists()
    assert not (student / ".cs351" / "pristine" / "a1" / "q_old").exists()


def test_begin_force_is_quiet_when_nothing_changed(student, course):
    """Re-running begin -f with nothing changed is ordinary, not a failure.

    `git commit` exits non-zero when nothing is staged and prints "nothing to
    commit" to stdout, not stderr -- so the student saw raw git output followed
    by a NOTE saying the commit failed, when everything was already in place.
    """
    run_begin(student, course, "a1")
    r = run_begin(student, course, "-f", "a1")
    assert r.returncode == 0, r.stderr
    assert "Could not commit" not in r.stderr
    assert "nothing to commit" not in r.stdout
    assert "nothing to commit" not in r.stderr


def test_begin_installs_reference_docs(student, course):
    """GRADING.md and WORKFLOW.md land in the student's own repository.

    They live in the course repository rather than the template so that they
    refresh: the template is copied once at repository creation and never
    updates. Copying them on every begin keeps them next to the student's work
    AND current, which is why a1's handout can link ../GRADING.md.
    """
    (course / "GRADING.md").write_text("v1 grading\n")
    (course / "WORKFLOW.md").write_text("v1 workflow\n")
    git(course, "add", "-A")
    git(course, "commit", "-q", "-m", "add references")

    r = run_begin(student, course, "a1")
    assert r.returncode == 0, r.stderr
    assert (student / "GRADING.md").read_text() == "v1 grading\n"
    assert (student / "WORKFLOW.md").read_text() == "v1 workflow\n"

    # committed, not left dangling for `save` to sweep up later
    tracked = git(student, "ls-files").stdout.split()
    assert "GRADING.md" in tracked
    assert "WORKFLOW.md" in tracked


def test_begin_refreshes_reference_docs(student, course):
    """An updated reference reaches a student who has already begun work."""
    (course / "GRADING.md").write_text("v1\n")
    git(course, "add", "-A")
    git(course, "commit", "-q", "-m", "references v1")
    run_begin(student, course, "a1")
    assert (student / "GRADING.md").read_text() == "v1\n"

    (course / "GRADING.md").write_text("v2\n")
    git(course, "add", "-A")
    git(course, "commit", "-q", "-m", "references v2")

    r = run_begin(student, course, "-f", "a1")
    assert r.returncode == 0, r.stderr
    assert (student / "GRADING.md").read_text() == "v2\n"


def test_begin_works_without_reference_docs(student, course):
    """A course repository lacking them must not break begin."""
    r = run_begin(student, course, "a1")
    assert r.returncode == 0, r.stderr
    assert (student / "a1" / "README.md").exists()
    assert not (student / "GRADING.md").exists()
