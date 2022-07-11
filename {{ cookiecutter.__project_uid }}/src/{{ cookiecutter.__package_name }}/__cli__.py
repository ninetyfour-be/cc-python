"""Command-line interface for {{ cookiecutter.project_name }}."""
import click
import {{ cookiecutter.__package_name }}


@click.command()
@click.version_option(version={{ cookiecutter.__package_name }}.__version__)
def main() -> None:
    """{{ cookiecutter.project_name }}."""


if __name__ == "__main__":
    main(prog_name="{{ cookiecutter.project_name }}") # pragma: no cover
