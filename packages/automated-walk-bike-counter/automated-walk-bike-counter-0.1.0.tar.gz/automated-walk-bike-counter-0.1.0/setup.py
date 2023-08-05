# Copyright (c) Data Science Research Lab at California State University Los
# Angeles (CSULA), and City of Los Angeles ITA
# Distributed under the terms of the Apache 2.0 License
# www.calstatela.edu/research/data-science
# Designed and developed by:
# Data Science Research Lab
# California State University Los Angeles
# Dr. Mohammad Pourhomayoun
# Mohammad Vahedi
# Haiyan Wang

"""The setup script."""

from os.path import exists

from setuptools import find_packages, setup

from automated_walk_bike_counter._version import __version__ as version

readme = open("README.md").read() if exists("README.md") else ""
requires = [
    line.strip()
    for line in open("requirements.txt").readlines()
    if not line.startswith("#")
]

develop_requires = [
    "pre-commit",
    "flake8",
    "black",
    "isort",
]

gpu_requires = ["tensorflow-gpu"]

setup(
    name="automated-walk-bike-counter",
    description=(
        "A computer vision application for automated counting"
        "of pedestrians and cyclists"
    ),
    long_description=readme,
    long_description_content_type="text/markdown",
    maintainer="CSULA and Los Angeles ITA",
    maintainer_email="",
    url="https://github.com/CityOfLosAngeles/automated-walk-bike-counter",
    packages=find_packages(),
    package_data={
        "automated_walk_bike_counter": [
            "core/data/*",
            "gui/static/images/*",
            "gui/static/videos/*",
        ],
    },
    package_dir={"automated_walk_bike_counter": "automated_walk_bike_counter"},
    include_package_data=True,
    install_requires=requires,
    extras_require={"develop": develop_requires, "gpu": gpu_requires},
    entry_points={
        "console_scripts": [
            "automated-walk-bike-counter = automated_walk_bike_counter.gui.app:main"
        ]
    },
    license="Apache-2.0 license",
    zip_safe=False,
    keywords="computer vision, city, streets, traffic, pedestrian, cyclist",
    version=version,
)
