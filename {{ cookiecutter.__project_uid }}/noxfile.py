"""Noxfile for {{ cookiecutter.project_name }}."""
from pathlib import Path
import platform
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
        try:
            shutil.rmtree(path)
        except Exception:
            pass


{% if cookiecutter.docker -%}
@nox.session(python=False)
def docker(session: nox.Session) -> None:
    """Build the Docker image."""
    import sys
    sys.path.insert(0, "src")
    from {{ cookiecutter.__package_name }} import __version__ as version

    tag = f"{{ cookiecutter.__project_slug }}:{version}"
    Path("build/docker").mkdir(parents=True, exist_ok=True)
    session.run("docker", "build", "--rm", "--tag", tag, ".")
    session.run("docker", "save", "--output", f"build/docker/{tag.replace(':', '_')}.tar", tag)
{%- endif %}


@nox.session(python=PYTHON_VERSIONS[0])
def executable(session: nox.Session) -> None:
    """Build an executable."""
    session.install("pyinstaller", ".")
    dist_path = str(Path(f"./build/{platform.system().lower().replace('darwin', 'macos')}")),
    build_path = str(Path(f"./tmp"))
    session.run(
        "pyinstaller",
        "src/{{ cookiecutter.__package_name }}/__cli__.py",
        "--clean",
        "--onefile",
        "--name",
        "{{ cookiecutter.__project_slug }}",
        "--console",
        "--distpath",
        dist_path,
        "--workpath",
        build_path,
    )
    {% if cookiecutter.gui -%}
    session.run(
        "pyinstaller",
        "src/{{ cookiecutter.__package_name }}/__gui__.py",
        "--clean",
        "--onefile",
        "--name",
        "{{ cookiecutter.__project_slug }}-gui",
        "--windowed",
        "--distpath",
        dist_path,
        "--workpath",
        build_path,
    )
    {%- endif %}
    shutil.rmtree("tmp")



@nox.session(python=False)
def release(session: nox.Session) -> None:
    """Build a release."""
    import sys
    sys.path.insert(0, "src")
    from {{ cookiecutter.__package_name }} import __version__ as version

    uid = f"{{ cookiecutter.__project_uid }}_{version}"
    name = f"{{ cookiecutter.__project_slug }}_{version}"
    # Build documentation
    session.run("nox", "-s", "doc")
    session.run(
        "cp",
        f"build/docs/{name}.pdf",
        f"{name}.pdf"
    )
    {% if cookiecutter.docker -%}
    # Build docker image
    session.run("nox", "-s", "docker")
    session.run(
        "cp",
        f"build/docker/{name}.tar",
        f"{name}.tar"
    )
    {%- endif %}
    session.run(
        "zip",
        "-r",
        "-9",
        f"{uid}.zip",
        f"{name}.pdf",
        {% if cookiecutter.docker -%}
        f"{name}.tar",
        "Dockerfile",
        {%- endif %}
        "pyproject.toml",
        "src",
        "tests",
        "build/windows",
        "build/linux",
        "-x",
        "**/__pycache__**",
        "**/{{ cookiecutter.__package_name }}.egg-info**",
    )
    session.run("rm", f"{name}.pdf"{% if cookiecutter.docker -%} , f"{name}.tar"{%- endif %})


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
