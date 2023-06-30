import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="xsskiller",
    version="1.1.1",
    description="Automated tool scans URLS parameters to check if reflected XSS is vulnerable",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/abeljm/XSSKiller",
    author="Avelino Navarro",
    author_email="abeljm2017@gmail.com",
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ],
    packages=["xsskiller"],
    include_package_data=True,
    install_requires=["colorama", "requests"],
    entry_points={
        "console_scripts": [
            "xsskiller=xsskiller.xsskiller:main",
        ]
    },
)
