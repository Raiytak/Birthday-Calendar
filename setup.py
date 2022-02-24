from setuptools import setup

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open(path.join(here, "requirements.txt"), encoding="utf-8") as f:
    requirements = f.read()

list_requirements = requirements.split("\n")

setup(
    name="birthday-calendar",
    version="1.0",
    python_requires=">=3.8",
    description="Calendar of birthdays using tkcalendar",
    long_description=long_description,
    url="https://github.com/Raiytak/Birthday-Calendar",
    author="Mathieu Salaun",
    author_email="mathieu.salaun12@gmail.com",
    keywords=["birthday", "calendar", "birthday calendar"],
    install_requires=list_requirements,
    packages=["birthday_calendar"],
)
