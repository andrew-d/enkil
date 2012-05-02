from __future__ import absolute_import

import os
import imp
import glob
import copy
import json

from .log import getLogger
from .depgraph import DependencyGraph, CycleException

log = getLogger(__name__)


class InfoClass(object):
    DEPENDENCIES = None

    def __init__(self):
        self.dependencies = type(self).DEPENDENCIES

    def get(self, info):
        log.error("Base class get() called!")
        raise NotImplemented("Base class get() called!")


def plugin_loader(exclude=[]):
    """Generator that loads all plugins"""
    module_path = os.path.dirname(__file__)
    for plugin_path in glob.iglob(os.path.join(module_path, "plugins", "*.py")):
        plugin_name = os.path.splitext(os.path.basename(plugin_path))[0]

        if plugin_name not in exclude:
            plugin = imp.load_source("enkil.plugins." + plugin_name, plugin_path)
            yield plugin


def get_base_info(info):
    module_path = os.path.dirname(__file__)

    # Load our base module - this allows us to load further files without errors.
    imp.load_source("enkil.plugins", os.path.join(module_path, "plugins", "__init__.py"))

    # Load the base plugin, and get the handlers.
    plugin = imp.load_source("enkil.plugins.base", os.path.join(module_path, "plugins", "base.py"))
    handlers = plugin.getHandlers(info)

    # Get information for each handler, and add it to the return dict.
    base_info = {"base": {}}
    for h in handlers:
        new_info = h().get(info)
        base_info['base'].update(new_info)

    # Return base info.
    return base_info


def load_plugins(base_info, exclude):
    log.debug("Loading plugins...")

    graph = DependencyGraph()

    # Load all plugins except the base plugin.
    for plugin in plugin_loader(exclude=exclude):
        plugin_name = plugin.__name__
        log.debug("Plugin: %r", plugin_name)

        try:
            handlers = plugin.getHandlers(base_info)
        except AttributeError:
            log.error("Could not get handlers for plugin: %s", plugin_name)
            continue

        log.info("Got handlers: %s", handlers)

        for handler in handlers:
            graph.add_node((plugin_name, handler()))

            if handler.dependencies is not None:
                graph.add_dependencies((plugin_name, handler), handler.dependencies)

    return graph


def main():
    log.debug("main() function started")

    # We get our base info first, since this can be used to make decisions
    # about which handlers we run.  Also make a copy for later.
    try:
        info = get_base_info({})
    except Exception, e:
        log.error("Error while loading base plugins: %s" % (e,))
        return

    given_info = copy.deepcopy(info)

    # Copy it to get base_info.  This is a copy, because we don't want any
    # getHandlers() functions modifying the information.
    base_info = copy.deepcopy(info)

    # Load each plugin, add the callable handlers to our dependency graph.
    depgraph = load_plugins(base_info, ['__init__', 'base'])

    # Get a topologically-sorted order for the dependency graph.
    try:
        order = depgraph.get_traversal()
    except CycleException, e:
        log.error(e)
        return

    log.debug("Plugin ordering is: %r", order)

    # Walk through the traversal, allowing each callable to update our info.
    # Note: each handler gets passed "given_info", but the returned information
    #       is placed into "info".  This is to stop a handler from modifying
    #       the info in the parameter and potentially stomping over other
    #       plugins' information.
    for plugin_name, handler in order:
        log.debug("Calling handler: %r", handler)

        if plugin_name not in info:
            info[plugin_name] = {}
            given_info[plugin_name] = {}

        new_info = handler.get(given_info)

        info[plugin_name].update(new_info)
        given_info[plugin_name].update(new_info)

    log.debug("main() function done")

    print json.dumps(info, indent=4)


if __name__ == "__main__":
    main()
