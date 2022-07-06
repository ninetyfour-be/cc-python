"""Noxfile for {{ cookiecutter.project_name }}."""
from pathlib import Path

import nox


nox.options.sessions = ["format", "lint", "test", "coverage"]

PYTHON_VERSIONS = ["3.8", "3.9", "3.10"]
SOURCES = ["src", "tests", "noxfile.py"]


@nox.session(python=PYTHON_VERSIONS[0])
def doc(session: nox.Session) -> None:
    """Build the documentation."""
    session.install("sphinx", "sphinx_click", "myst-parser", "rinohtype", ".")
    args = session.posargs or ["rinoh"]
    session.run("sphinx-build", "-b", args[0], "docs", "build/docs")


@nox.session(python=PYTHON_VERSIONS[0], reuse_venv=True)
def format(session: nox.Session) -> None:
    """Format the code."""
    session.install("black", "isort")
    args = session.posargs or SOURCES
    session.run("black", "--target-version", "py38", *args)
    session.run("isort", "--profile", "black", *args)


@nox.session(python=PYTHON_VERSIONS[0], reuse_venv=True)
def lint(session: nox.Session) -> None:
    """Lint the code."""
    session.install(
        "flake8", "darglint", "flake8-docstrings", "flake8-bugbear", "pep8-naming"
    )
    args = session.posargs or SOURCES
    session.run(
        "flake8",
        "--jobs",
        "auto",
        "--max-complexity",
        "10",
        "--max-line-length",
        "88",
        "--extend-ignore",
        "E203",
        "--docstring-convention",
        "numpy",
        "--docstring-style",
        "numpy",
        "--strictness",
        "long",
        "--doctests",
        *args,
    )


@nox.session(python=PYTHON_VERSIONS)
def test(session: nox.Session) -> None:
    """Run the tests."""
    session.install("pytest", "coverage", ".")
    session.run("coverage", "run", "-p", "-m", "pytest", "tests")
    session.notify("coverage")


@nox.session(python=PYTHON_VERSIONS[0], reuse_venv=True)
def coverage(session: nox.Session) -> None:
    """Build the coverage report."""
    if Path().glob(".coverage.*"):
        session.install("coverage")
        session.run("coverage", "combine")
        session.run("coverage", "report", "--show-missing" "--fail-under=80")
