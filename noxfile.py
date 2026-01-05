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
def benchmarks(session):
    """
    Run benchmark tests.
    """
    session.run("poetry", "install", "-E", "pandas", external=True)
    session.run("pytest -m benchmark")

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
