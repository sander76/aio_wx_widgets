"""Nox testing."""

import nox


def install_flit_dev_deps(session):
    session.install("flit")
    session.run("flit", "install", "--deps", "develop")


@nox.session(python=["3.7", "3.8"])
def tests(session):
    install_flit_dev_deps(session)
    session.run("pytest", "--cov=aio_wx_widgets", "--cov-report=html", "tests")


@nox.session(python=["3.7"])
def pylint(session):
    install_flit_dev_deps(session)
    session.run("pylint", aio_wx_widgets)
