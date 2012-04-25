"""
This plugin is the "base" plugin - it provides the most basic information
needed to bootstrap other plugins.  Specifically, it provides:

 - Python version
 - Operating system and version
 - Host name and FQDN

"""

import socket
import platform

from enkil.log import getLogger

log = getLogger(__name__)


def getPythonVersion(info):
    return {
        "python_version": platform.python_version()
    }


def getHostNameInfo(info):
    return {
        "hostname": socket.gethostname(),
        "fqdn": socket.getfqdn()
    }


def getOsVersionInfo(info):
    log.warn("Test")
    return {
        "platform": {
            "name": platform.system().lower(),
            "release": platform.release().lower(),
            "version": platform.version().lower(),
            "fullname": platform.platform(),
        }
    }


def getHandlers(base_info):
    log.debug("base getHandlers() called")

    return [
        (getPythonVersion, None),
        (getHostNameInfo, None),
        (getOsVersionInfo, None),
    ]
