"""Sphinx configuration for {{ cookiecutter.project_name }}."""
import sys
sys.path.insert(0, "..")
from {{ cookiecutter.__package_name }} import __version__ as version


project = "{{ cookiecutter.project_name }}"
author = "Ninety Four"
copyright = "{% now 'utc', '%Y' %}, Ninety Four"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
    "rinoh.frontend.sphinx",
]
rinoh_documents = [
    dict(
        doc="index",
        target=f"{{ cookiecutter.__project_slug }}_{version}",
        title=project,
        subtitle=f"v{version}",
        date="",
        domain_indices=False,
    ),
]
