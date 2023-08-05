################################################################################
# Copyright (C) 2016-2020 Abstract Horizon
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License v2.0
# which accompanies this distribution, and is available at
# https://www.apache.org/licenses/LICENSE-2.0
#
#  Contributors:
#    Daniel Sendula - initial API and implementation
#
#################################################################################

from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="pyros-client",
    version="1.0.0",
    author="Daniel Sendula",
    description="Support library for PyROS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Abstract-Horizon/pyros-client",
    zip_safe=False, # Doesn't create an egg - easier to debug and hack on
    packages=['pyros', 'pyroslib'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
