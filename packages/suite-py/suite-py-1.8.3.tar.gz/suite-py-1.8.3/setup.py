#################### Maintained by Hatch ####################
# This file is auto-generated by hatch. If you'd like to customize this file
# please add your changes near the bottom marked for 'USER OVERRIDES'.
# EVERYTHING ELSE WILL BE OVERWRITTEN by hatch.
#############################################################
from io import open

from setuptools import find_packages, setup

from suite_py import version


with open("README.rst", "r", encoding="utf-8") as f:
    readme = f.read()

REQUIRES = [
    "prima-youtrack==0.2.4",
    "PyGithub>=1.51",
    "cement>=3.0",
    "PyInquirer>=1.0.3",
    "PyYaml>=5.1,<5.3",
    "termcolor>=1.1.0",
    "autoupgrade-prima>=0.5.1",
    "semver>=2.9.0",
    "halo>=0.0.28",
    "boto3>=1.11.13",
    "awscli>=1.17.13",
    "Click>=7.0",
    "pptree==3.1",
    "Jinja2>=2.11",
]

kwargs = {
    "name": "suite-py",
    "version": version,
    "description": "",
    "long_description": readme,
    "author": "Prima Assicurazioni S.p.A",
    "author_email": "devops@prima.it",
    "maintainer": "larrywax, EugenioLaghi, michelangelomo",
    "maintainer_email": "devops@prima.it",
    "url": "https://github.com/primait/suite_py",
    "license": "MIT/Apache-2.0",
    "classifiers": [
        # 'Development Status :: 4 - Beta',
        # 'Intended Audience :: Developers',
        # 'License :: OSI Approved :: MIT License',
        # 'License :: OSI Approved :: Apache Software License',
        # 'Natural Language :: English',
        # 'Operating System :: OS Independent',
        # 'Programming Language :: Python :: 3.5',
        # 'Programming Language :: Python :: 3.6',
        # 'Programming Language :: Python :: Implementation :: CPython',
        # 'Programming Language :: Python :: Implementation :: PyPy',
    ],
    "install_requires": REQUIRES,
    "tests_require": ["coverage", "pytest"],
    "packages": find_packages(exclude=("tests", "tests.*")),
    "entry_points": {"console_scripts": ["suite-py = suite_py.cli:main",],},
}

#################### BEGIN USER OVERRIDES ####################
# Add your customizations in this section.

###################### END USER OVERRIDES ####################

setup(**kwargs)
