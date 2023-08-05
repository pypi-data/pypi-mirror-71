"""
globalarrays: Global Arrays Toolkit
===================================

- globalarrays
    The Global Arrays Toolkit shared library

 Global Arrays (GA) is a Partitioned Global Address Space (PGAS)
 programming model. It provides primitives for one-sided communication
 (Get, Put, Accumulate) and Atomic Operations (read increment).
 It supports blocking and non-blocking primtives, and supports location
 consistency.

 Starting with GA v5.4, ARMCI has been deprecated and replaced with
 Communication runtime for Extreme Scale (ComEx). GA uses ComEx
 to abstract inter-node communication operations.
 The default ComEx ports use MPI --- which makes GA and ComEx
 portable for high-end systems.
 Most ComEx implementations use on-node shared memory for faster
 intra-node communication.

 This Release:

    March 30, 2018 5.7

"""

import os
import sys
from distutils.spawn import find_executable
from distutils.dir_util import mkpath
from distutils import log
from setuptools import setup
from setuptools.command.install import install as Install

PKGNAME = "globalarrays"
SUBVERSION = '0b1'
REQFILE = "requirements.txt"
CONFIGURE_OPTIONS = ['--enable-shared']
__INIT__ = """
# Author:  Roberto Vidmar
# Contact: rvidmar@inogs.it

raise RuntimeError("Module cannot be imported, it provides only the"
        " Global Arrays Toolkit library")
"""

#------------------------------------------------------------------------------
def version():
    return "5.7.%s" % SUBVERSION

#------------------------------------------------------------------------------
def bootstrap():
    # Generate package __init__.py file
    pkgdir = os.path.join('config', 'pypi')
    if not os.path.exists(pkgdir):
        mkpath(pkgdir)
    pkgfile = os.path.join(pkgdir, '__init__.py')
    fh = open(pkgfile, 'w')
    fh.write(__INIT__)
    fh.close()

#------------------------------------------------------------------------------
def execute(command):
    """ Execute system command and exit on error
    """
    status = os.system(command)
    if status != 0:
        raise RuntimeError(status)

#------------------------------------------------------------------------------
def configure(prefix, dry_run=False):
    log.info('Configuring %s for %s...' % (PKGNAME, prefix))
    options = ["--prefix=%s" % prefix]
    options.extend(CONFIGURE_OPTIONS)

    log.info('configure options:')
    for opt in options:
        log.info(' ' * 4 + opt)
    if dry_run:
        return

    # Swtich to package source dir
    os.chdir("ga-master")

    execute('./autogen.sh')
    command = ['./configure'] + options
    execute(" ".join(command))
    log.debug("\n\n%s configured.\n" % PKGNAME)

#------------------------------------------------------------------------------
def build(dry_run=False):
    log.info('Building GA...')
    if dry_run:
        return

    make = find_executable('make')
    execute(make)
    log.debug("\n\n%s built.\n" % PKGNAME)

#------------------------------------------------------------------------------
def install(dry_run=False):
    log.info('Installing GA...')
    if dry_run:
        return

    make = find_executable('make')
    execute("%s install" % make)
    log.debug("\n\n%s installed.\n" % PKGNAME)

#------------------------------------------------------------------------------
#==============================================================================
class Context:
    def __init__(self):
        # Save arguments
        self.sys_argv = sys.argv[:]
        # And current direcory
        self.cwd = os.getcwd()

    def enter(self):
        del sys.argv[1:]
        return self

    def exit(self):
        # Restore arguments
        sys.argv[:] = self.sys_argv
        # And directory
        os.chdir(self.cwd)

#==============================================================================
class CustomInstall(Install):
    """Custom handler for the 'install' command
    """
    def initialize_options(self):
        super().initialize_options()
        self.optimize = 1

    def finalize_options(self):
        super().finalize_options()
        self.install_lib = self.install_platlib
        self.install_libbase = self.install_lib

    def run(self):
        # self.install_lib is .../venv/lib/python3.6/site-packages/
        root_dir = os.path.abspath(self.install_lib)
        prefix = os.path.join(root_dir, PKGNAME)
        ctx = Context().enter()
        try:
            configure(prefix, self.dry_run)
            build(self.dry_run)
            install(self.dry_run)
        finally:
            ctx.exit()

        self.outputs = []
        # These are the installed files
        for dirpath, _, filenames in os.walk(prefix):
            for fn in filenames:
                self.outputs.append(os.path.join(dirpath, fn))
        super().run()

    def get_outputs(self):
        outputs = getattr(self, 'outputs', [])
        outputs += super().get_outputs()
        return outputs

#==============================================================================
description = __doc__.split('\n')[1:-1][0]
classifiers = """
Development Status :: 4 - Beta
Intended Audience :: Developers
Intended Audience :: Science/Research
License :: OSI Approved :: BSD License
Operating System :: POSIX
Programming Language :: C
Programming Language :: C++
Programming Language :: Fortran
Programming Language :: Python
Topic :: Scientific/Engineering
Topic :: Software Development :: Libraries
"""

if 'bdist_wheel' in sys.argv:
    sys.stderr.write("%s: this package cannot be built as a wheel\n"
            % PKGNAME)
    sys.exit(1)

bootstrap()

with open(REQFILE) as fp:
    requirements = fp.read()

setup(name=PKGNAME,
        version=version(),
        install_requires=requirements,
        description=description,
        long_description=open("README.md", "r").read(),
        long_description_content_type='text/markdown',
        classifiers=classifiers.split('\n')[1:-1],
        keywords=['GlobalArrays', 'MPI'],
        platforms=['POSIX'],
        license='BSD',
        include_package_data=True,
        url='https://hpc.pnl.gov/globalarrays/',
        download_url='https://hpc.pnl.gov/globalarrays/download.shtml',

        author=("Jarek Nieplocha, Bruce Palmer, Vinod Tipparaju,"
            " Manojkumar Krishnan, Harold Trease, and Edo Apra"),
        author_email='hpctools@googlegroups.com',
        maintainer='Roberto Vidmar',
        maintainer_email='rvidmar@inogs.it',

        packages=[PKGNAME],
        package_dir={PKGNAME: 'config/pypi'},
        cmdclass={'install': CustomInstall},
        )
