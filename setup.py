from setuptools import setup

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="birthday_calendar",
    version="1.0",
    python_requires=">=3.8",
    description="Calendar of birthdays using tkcalendar",
    long_description=long_description,
    url="https://github.com/Raiytak/Birthday-Calendar",
    author="Mathieu Salaun",
    author_email="mathieu.salaun12@gmail.com",
    keywords=["birthday", "calendar", "birthday calendar"],
    install_requires=["googletrans>=4.0.0-rc1"],
    packages=["birthday_calendar"],
)
