#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

package = "pydemic"


# authoritative version in pytools/__init__.py
def find_git_revision(tree_root):
    # Keep this routine self-contained so that it can be copy-pasted into
    # setup.py.

    from os.path import join, exists, abspath
    tree_root = abspath(tree_root)

    if not exists(join(tree_root, ".git")):
        return None

    from subprocess import Popen, PIPE, STDOUT
    p = Popen(["git", "rev-parse", "HEAD"], shell=False,
              stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True,
              cwd=tree_root)
    (git_rev, _) = p.communicate()

    import sys
    if sys.version_info >= (3,):
        git_rev = git_rev.decode()

    git_rev = git_rev.rstrip()

    retcode = p.returncode
    assert retcode is not None
    if retcode != 0:
        from warnings import warn
        warn("unable to find git revision")
        return None

    return git_rev


def write_git_revision(package_name):
    from os.path import dirname, join
    dn = dirname(__file__)
    git_rev = find_git_revision(dn)

    with open(join(dn, package_name, "_git_rev.py"), "w") as outf:
        outf.write("GIT_REVISION = %s\n" % repr(git_rev))


write_git_revision(package)

setup(
    name=package,
    version="2020.2.1",
    description="A python driver for epidemic modeling and inference",
    long_description=open("README.rst", "rt").read(),
    install_requires=[
        "numpy",
        "scipy",
        "pandas",
        "emcee",
        "h5py",
        "tables",
    ],
    url='https://github.com/uiuc-covid19-modeling/pydemic',
    author="Zachary J Weiner, George N Wong",
    license="MIT",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    packages=find_packages(),
    python_requires='>=3',
    project_urls={
        'Documentation': 'https://pydemic.readthedocs.io/en/latest/',
        'Source': 'https://github.com/uiuc-covid19-modeling/pydemic',
    },
)
