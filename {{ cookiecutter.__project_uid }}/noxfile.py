"""Noxfile for {{ cookiecutter.project_name }}."""
from pathlib import Path
import shutil

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
    # Clean build
    for path in Path("build").glob("**/*[!(.pdf)]"):
        if path.is_file():
            path.unlink()
    for path in [Path("build") / p for p in {"lib", "bdist.linux-x86_64", "docs/.doctrees"}]:
        shutil.rmtree(path)


@nox.session(python=False)
def release(session: nox.Session) -> None:
    """Build a release."""
    import sys
    sys.path.insert(0, "src")
    from {{ cookiecutter.__package_name }} import __version__ as version

    session.run("nox", "-s", "doc")
    session.run(
        "cp",
        f"build/docs/{{ cookiecutter.__project_slug }}_{version}.pdf",
        f"{{ cookiecutter.__project_slug }}_{version}.pdf"
    )
    session.run(
        "zip",
        "-r",
        "-9",
        f"{{ cookiecutter.__project_uid }}_{version}.zip",
        f"{{ cookiecutter.__project_slug }}_{version}.pdf",
        "pyproject.toml",
        "src",
        "tests",
        "-x",
        "**/__pycache__**",
        "**/{{ cookiecutter.__package_name }}.egg-info**",
    )
    session.run("rm", f"{{ cookiecutter.__project_slug }}_{version}.pdf")


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
