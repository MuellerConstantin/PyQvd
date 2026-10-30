# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# The project is installed in the documentation environment, both on Read the Docs and in the
# nox session, so it is imported from there instead of being put on the path manually. The module
# is imported as a whole, as a top-level name like `version` would be read as a Sphinx config value.
import importlib.metadata

project = "PyQvd"
copyright = "2024, Constantin Müller"
author = "Constantin Müller"
# Taken from the installed project, so pyproject.toml remains the single source of the version
release = importlib.metadata.version("pyqvd")

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc"
]

templates_path = ["_templates"]
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
