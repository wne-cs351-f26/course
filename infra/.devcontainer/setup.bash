#!/usr/bin/env bash
# Installs the CS351 commands into a student's codespace.
#
# Runs once at container creation. Clones the course repository (starter
# code plus the begin/save commands) and links the commands onto PATH.
set -euo pipefail

COURSE_URL="https://github.com/wne-cs351-f26/course.git"
COURSE_DIR="${HOME}/.local/share/cs351/course"

mkdir -p "${HOME}/.local/bin" "$(dirname "${COURSE_DIR}")"

if [[ -d "${COURSE_DIR}/.git" ]]; then
    git -C "${COURSE_DIR}" pull --ff-only
else
    git clone --quiet "${COURSE_URL}" "${COURSE_DIR}"
fi

shopt -s nullglob
linked=0
for command in "${COURSE_DIR}"/bin/*; do
    ln -sf "${command}" "${HOME}/.local/bin/$(basename "${command}")"
    linked=$((linked + 1))
done

if [[ "${linked}" -eq 0 ]]; then
    echo "No CS351 commands found. 'begin' and 'save' will not work — tell your instructor." >&2
fi

{
    echo "export CS351_COURSE=\"${COURSE_DIR}\""
    echo "export CS351_REPO_ROOT=\"\${CONTAINER_WORKSPACE_FOLDER:-\$PWD}\""
    echo 'export PATH="${HOME}/.local/bin:${PATH}"'
} >> "${HOME}/.bashrc"

echo "CS351 environment ready. Run 'begin' to list assignments."
