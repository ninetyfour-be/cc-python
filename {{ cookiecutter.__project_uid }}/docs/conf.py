"""Sphinx configuration for {{ cookiecutter.project_name }}."""
import sys

sys.path.insert(0, "..")

project = "{{ cookiecutter.project_name }}"
author = "Ninety Four"
copyright = "{% now 'utc', '%Y' %}, Ninety Four"
version = "0.1.0"
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
        target="{{ cookiecutter.__project_slug }}",
        title=project,
        subtitle=f"v{version}",
        date="",
        domain_indices=False,
    ),
]
