"""
Contains nox sessions.
"""

import nox

@nox.session
def tests(session):
    """
    Run tests.
    """
    session.run("poetry", "install", "-E", "pandas", external=True)
    session.run("pytest")

@nox.session
def benchmark(session):
    """
    Run benchmark tests.
    """
    session.run("poetry", "install", "-E", "pandas", external=True)
    session.run("pytest", "-m", "benchmark", "--benchmark-autosave",
                "--benchmark-warmup=on", "--benchmark-warmup-iterations=1")

@nox.session
def profiling(session):
    """
    Run profiling tests.
    """
    session.run("poetry", "install", "-E", "pandas", external=True)
    session.run("pytest", "-m", "profiling", "-s")

@nox.session
def lint(session):
    """
    Run linter.
    """
    session.run("poetry", "install", "-E", "pandas", external=True)
    session.run("pylint", "pyqvd", "tests")

@nox.session
def build(session):
    """
    Build package.
    """
    session.run("poetry", "build", external=True)

@nox.session
def docs(session):
    """
    Build documentation with Sphinx.
    """
    session.run("poetry", "install", "-E", "pandas", external=True)
    session.install("-r", "docs/requirements.txt", external=True)

    session.run(
        "sphinx-build",
        "-b", "html",
        "docs/source",
        "docs/_build/html",
    )
