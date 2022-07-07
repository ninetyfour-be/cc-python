# Usage

This chapter describes how to use the project once you are done installing its dependencies. To use it, you first need to activate the virtual environment as described in the installation instructions.

## Command-line interface

```{eval-rst}
.. click:: {{ cookiecutter.__package_name }}.__cli__:main
    :prog: {{ cookiecutter.__project_slug }}
    :nested: full
```

{% if cookiecutter.docker -%}
## Using Docker

If you decided to use the *Docker* image, you can run the command by spawning a container. This is achieved with the following command:
```
docker run --rm {{ cookiecutter.__project_slug }}:VERSION [OPTIONS]
```
where you must replace `VERSION` by the version of the image you want to use.
{%- endif %}
