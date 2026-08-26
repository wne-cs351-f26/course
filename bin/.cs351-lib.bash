# Shared helpers for begin and save.
#
# This file is named with a leading dot deliberately: setup.bash installs
# commands onto a student's PATH by globbing "${COURSE_DIR}/bin/*", and a
# bare `*` glob does not match dotfiles unless `dotglob` is set. That keeps
# this library out of ~/.local/bin -- it is meant to be sourced, not run.
#
# Callers must source it via a symlink-resolved path to their own location,
# e.g.:
#   _self="$(readlink -f "${BASH_SOURCE[0]}")"
#   source "$(dirname "${_self}")/.cs351-lib.bash"
# because begin/save are themselves symlinked onto PATH, and BASH_SOURCE
# would otherwise resolve to the symlink's directory, not this one.

# True (exit 0) if REPO_ROOT looks like a git repository at all.
# Wrapped in a brace group so bash parses the whole file before executing any
# of it: a `begin` run pulls the course repository, which rewrites every file
# in bin/ -- including this one -- and bash would otherwise resume reading at
# an offset into the new content. See the longer note in `begin`.
{
# The top level of the repository containing `start`, or `start` itself when it
# is not in one (so callers can still report a sensible path in their error).
#
# CS351_REPO_ROOT is exported from ~/.bashrc as ${CONTAINER_WORKSPACE_FOLDER:-$PWD},
# and CONTAINER_WORKSPACE_FOLDER is NOT set in this image -- so its value is
# whatever $PWD happened to be when .bashrc was sourced. Start a shell from
# inside src/a1 and the variable points at src/a1, which would have begin
# writing src/a1/src/a1 and syncing course files into the student's own
# assignment directory. Resolving to the top level makes the variable a hint
# rather than something that has to be right.
cs351_resolve_repo_root() {
    local start="${1}" top
    top="$(git -C "${start}" rev-parse --show-toplevel 2>/dev/null || true)"
    if [[ -n "${top}" ]]; then
        printf '%s\n' "${top}"
    else
        printf '%s\n' "${start}"
    fi
}


cs351_is_git_repo() {
    git -C "${1}" rev-parse --git-dir >/dev/null 2>&1
}

# Prints the absolute path to REPO_ROOT's git directory (handles worktrees).
cs351_repo_git_dir() {
    local repo_root="${1}" git_dir
    git_dir="$(git -C "${repo_root}" rev-parse --git-dir)"
    (cd "${repo_root}" && cd "${git_dir}" && pwd)
}

# True (exit 0) if REPO_ROOT is mid-merge, mid-rebase, or has any unresolved
# (unmerged) paths left over from a conflict that was never finished. This
# is the exact condition that makes `git commit` refuse a partial commit.
cs351_repo_has_unfinished_merge() {
    local repo_root="${1}" git_dir
    git_dir="$(cs351_repo_git_dir "${repo_root}")"
    [[ -e "${git_dir}/MERGE_HEAD" ]] \
        || [[ -d "${git_dir}/rebase-merge" ]] \
        || [[ -d "${git_dir}/rebase-apply" ]] \
        || [[ -n "$(git -C "${repo_root}" ls-files -u)" ]]
}
}
