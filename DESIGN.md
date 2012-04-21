Design
======

This document will attempt to give a high-level overview of how Enkil is designed.  Once a stable version has been reached, this document will be updated with the final design and API.

General Ideas
-------------

In general, Enkil is concerned with gathering information from the system it's being run on.  It does this through the use of plugins, each of which is responsible for gathering one particular type or piece of information.  The gathered information is then exported in JSON format by printing to stdout.

Internally, information is represented as hierarchical nodes, in the format "a.b.c.d".  Each plugin registers itself as a provider of one particular node of information when it is loaded.  Then, once all plugins are loaded, Enkil will run each of them to obtain the relevant information provided.  Plugins are not run in a specified order (except base plugins, which are mentioned below), and should be relatively independent.  Plugin failures are expected and do not cause Enkil to fail, although a warning will be printed to stderr for each failing plugin.

Base plugins are special types of plugins that are run before all non-base plugins.  They are responsible for gathering information that non-base plugins may use to determine what to run - for example, the current operating system, architecture, Python version, and so on.  Base plugins are not run in any specific order, but it is guaranteed that all base plugins will run before any non-base plugins.  Furthermore, unlike non-base plugins, a failure in a base plugin is a critical failure and will cause Enkil to halt immediately.