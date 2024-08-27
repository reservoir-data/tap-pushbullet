"""Nox configuration."""

from __future__ import annotations

import sys

import nox

GITHUB_ACTIONS = "GITHUB_ACTIONS"

package = "tap-pushbullet"
src_dir = "tap_pushbullet"
tests_dir = "tests"

python_versions = [
    "3.13",
    "3.12",
    "3.11",
    "3.10",
    "3.9",
    "3.8",
]
main_python_version = "3.12"
locations = src_dir, tests_dir, "noxfile.py"

nox.needs_version = ">=2024.4.15"
nox.options.default_venv_backend = "uv"
nox.options.sessions = (
    "mypy",
    "tests",
)


@nox.session(python=python_versions)
def mypy(session: nox.Session) -> None:
    """Check types with mypy."""
    args = session.posargs or [src_dir, tests_dir]
    session.run("uv", "run", "mypy", *args)
    if not session.posargs:
        session.run(
            "uv",
            "run",
            "mypy",
            f"--python-executable={sys.executable}",
            "noxfile.py",
        )


@nox.session(python=python_versions)
def tests(session: nox.Session) -> None:
    """Execute pytest tests and compute coverage."""
    session.run(
        "uv",
        "run",
        "--verbose",
        "--python",
        f"python{session.python}",
        "pytest",
        *session.posargs,
    )
