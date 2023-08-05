#!/usr/bin/python
# Copyright (c) 2018 The Ontario Institute for Cancer Research. All rights
# reserved.
#
# This program and the accompanying materials are made available under the
# terms of the GNU Public License v3.0.
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,  BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""
from __future__ import print_function, absolute_import

# To use a consistent encoding
from codecs import open as open_
from os import path
import os
import sys
import xml.etree.ElementTree as ET
from datetime import datetime as dt

# Always prefer setuptools over distutils
from setuptools import setup
REQUIRED_PY_VERSION = (3, 6, 0)

# ------------- Version extraction ----------------
# Extract the version from the root pom.xml file
# -------------------------------------------------
def get_version_from_pom(pom_loc):
    tree = ET.parse(pom_loc)
    root = tree.getroot()
    for child in root:
        if 'version' in child.tag:
            print("version is: "+child.text)
            return child.text

def writeToFile(content, path):
    parent_dest_dir = os.path.dirname(path)
    if parent_dest_dir != "" and not parent_dest_dir.startswith('./'):
        os.makedirs(parent_dest_dir, exist_ok=True)
    with open(path, "w") as f_output:
        f_output.write(content)

def read_file_contents(path):
    contents = ""
    with open(path, "r") as fh:
        for line in fh.readlines():
            contents += line
    return contents

def get_required_py_version_string():
    return ".".join([str(i) for i in REQUIRED_PY_VERSION])

def get_current_py_version_string():
    v = sys.version_info
    return ".".join([str(v.major), str(v.minor), str(v.micro)])

def resolve_version():
    here = path.abspath(path.dirname(__file__))
    pom_loc = '../pom.xml'
    pom_path = path.join(here, pom_loc) 
    version_path = path.join(here, 'VERSION') 
    if path.isfile(pom_path):
        temp = get_version_from_pom(pom_path)
        writeToFile(temp, version_path)
    
    # This step is needed to persist the VERSION file in the distribution
    if path.isfile(version_path):
        return read_file_contents(version_path)
    else:
        raise Exception("VERSION file does not exist")

def resolve_description():
    here = path.abspath(path.dirname(__file__))
    description_path = path.join(here, 'README.md') 
    if path.isfile(description_path):
        return read_file_contents(description_path)
    else:
        raise Exception("The file %s does not exist" % description_path)

def run():
    """
    Run the setup program
    """
    here = path.abspath(path.dirname(__file__))

    if sys.version_info < REQUIRED_PY_VERSION:
        raise Exception(
            "[UNSUPPORTED_PY_VERSION]: Installation requires python >= {}, "
            "but the current version is {}".format(get_required_py_version_string(), get_current_py_version_string()))

    setup(
        name='overture-song',
        # Versions should comply with PEP440.  For a discussion on
        # single-sourcing the version across setup.py and the project code,
        # see
        # https://packaging.python.org/en/latest/single_source_version.html
        version=resolve_version(),
        description="A Python library interface to the SONG REST Server",
        long_description=resolve_description(),
        long_description_content_type='text/markdown',

        # The project's main homepage.
        url='https://github.com/overture-stack/SONG',

        # Author details
        author='Robert Tisma',
        author_email='Robert.Tisma@oicr.on.ca',

        # Choose your license
        license='License :: OSI Approved :: GNU General Public '
                'License v3 (GPLv3)',

        # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
        classifiers=[
            # How mature is this project? Common values are
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 3 - Alpha',

            # Indicate who your project is intended for
            'Intended Audience :: Developers',

            # Pick your license as you wish (should match "license" above)
            'License :: OSI Approved :: GNU General Public License '
            'v3 (GPLv3)',

            # Specify the Python versions you support here. In particular,
            # ensure that you indicate whether you support Python 2,
            # Python 3 or both.
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 3',
        ],

        # What does your project relate to?
        keywords='overture_song rest-client python-sdk song metadata',

        # You can just specify the packages manually here if your project is
        # simple. Or you can use find_packages().
        # packages=find_packages(exclude=['contrib', 'docs', 'tests']),
        packages=['overture_song'],

        # Alternatively, if you want to distribute just a my_module.py,
        # uncomment this:
        # py_modules=["my_module"],

        # List run-time dependencies here.  These will be installed by pip
        # when your project is installed. For an analysis of
        # "install_requires" vs pip's requirements files see:
        # https://packaging.python.org/en/latest/requirements.html
        install_requires=['requests>=2.20.0', 'dataclasses>=0.4'],

        # List additional groups of dependencies here (e.g. development
        # dependencies). You can install these using the following syntax,
        # for example:
        # $ pip install -e .[dev,test]
        extras_require={
        },

        # If there are data files included in your packages that need to be
        # installed, specify them here.  If using Python 2.6 or less, then
        # these have to be included in MANIFEST.in as well.
        package_data={
        },

        python_requires=">={}".format(get_required_py_version_string()),

        # Although 'package_data' is the preferred approach, in some case you
        # may need to place data files outside of your packages. See:
        # http://docs.python.org/3.4/distutils/
        #       setupscript.html#installing-additional-files # noqa
        # In this case, 'data_file' will be installed into
        # '<sys.prefix>/my_data'
        # To provide executable scripts, use entry points in preference to
        # the "scripts" keyword. Entry points provide cross-platform support
        # and allow pip to create the appropriate form of executable for the
        # target platform.
        entry_points={
        },
    )


if __name__ == "__main__":
    run()
