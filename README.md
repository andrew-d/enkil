Enki
====

Enki is a Python module designed to gather information about the running system.  It's similar to (and inspired by) the projects [ohai](https://github.com/opscode/ohai) and [facter](https://github.com/puppetlabs/facter).

Note: Enki is still very much in development, so it may not work on your system.  If you come across a bug (even just a small error!), please open an issue to let me know, and I'll do my best to fix it.

Design Goals
------------

  * Simple and extensible
  * Cross-platform (Linux, OS X, and Windows)
  * Minimal - the core should be as small as possible, with as much of the logic in plugins as possible
  * Flexible - should not fail if external modules are not installed

Author
------

Andrew Dunham - http://du.nham.ca/