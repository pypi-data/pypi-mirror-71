# Lint as: python3
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Config file for distributing package via Pypi server."""

import setuptools

with open("../README.md", "r") as fh:
  long_description = fh.read()

print(long_description)

setuptools.setup(
    name="gps-building-blocks",
    version="0.1.5",
    author="gPS Team",
    author_email="no-reply@google.com",
    description="Modules and tools useful for use with advanced data solutions on Google Ads, Google Marketing Platform and Google Cloud.",
    long_description=long_description,
    long_description_tpye="text/markdown",
    url="https://github.com/google/gps_building_blocks",
    license="Apache Software License",
    packages=setuptools.find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
    ],
)
