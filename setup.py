from setuptools import setup, find_packages
import io
import os

VERSION = "0.1"


def get_long_description():
    with io.open(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
            encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="dbf-cli",
    description="CLI tool for converting DBF files (dBase, FoxPro etc) to SQLite",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    version=VERSION,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'dbf-cli = dbf_cli.cli:dbf_cli',
        ]
    },
    install_requires=["dbf", "dbfread", "click", "sqlite_utils"],
)
