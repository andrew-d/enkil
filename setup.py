import distutils.core
import sys

# Try to import setuptools, but don't fail if we can't.
try:
    import setuptools
except ImportError:
    pass

kwargs = {}
major, minor = sys.version_info[:2]

# We must have setuptools for Python 3+
if major >= 3:
    import setuptools  
    kwargs["use_2to3"] = True

# Version up here for potential automatic stuff.
VERSION = '0.0.1'

# Extensions.
extensions = []

# Call our setup.
distutils.core.setup(
    name="enkil",
    version=VERSION,
    packages = ["enkil"],
    ext_modules = extensions,
    author="Andrew D",
    url="http://github.com/andrew-d/enkil",
    download_url="https://github.com/andrew-d/enkil/tarball/master",
    license="http://www.apache.org/licenses/LICENSE-2.0",
    description="Enkil is a Python module designed to gather information about a running system.",
    classifiers = [
        "Topic :: System :: Systems Administration",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Development Status :: 1 - Planning",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License"
    ],
    **kwargs
)
