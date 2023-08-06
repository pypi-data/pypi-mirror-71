# pylint: disable=missing-docstring

from setuptools import find_packages, setup

with open("README.rst", "rb") as fp:
    LONG_DESCRIPTION = fp.read().decode("utf-8").strip()

setup(
    name="pytest_polarion_collect",
    use_scm_version=True,
    url="https://gitlab.com/mkourim/pytest-polarion-collect",
    description="pytest plugin for collecting polarion test cases data",
    long_description=LONG_DESCRIPTION,
    author="Martin Kourim",
    author_email="mkourim@redhat.com",
    license="MIT",
    packages=find_packages(exclude=("tests",)),
    setup_requires=["setuptools_scm"],
    install_requires=["pytest", "polarion-docstrings>=0.21.0", "polarion-tools-common"],
    entry_points={
        "pytest11": [
            "pytest_polarion_collect = pytest_polarion_collect.polarion_collect",
            "pytest_polarion_collect_hooks = pytest_polarion_collect.collector_hooks",
        ]
    },
    keywords=["polarion", "py.test", "pytest", "testing"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Pytest",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: Developers",
    ],
    include_package_data=True,
)
