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
from enkil.main import InfoClass

log = getLogger(__name__)


class PythonVersion(InfoClass):
    DEPENDENCIES = None

    def get(self, info):
        return {
            "python_version": platform.python_version()
        }


class HostName(InfoClass):
    DEPENDENCIES = None

    def get(self, info):
        return {
            "hostname": socket.gethostname(),
            "fqdn": socket.getfqdn()
        }


class OsVersion(InfoClass):
    DEPENDENCIES = None

    def get(self, info):
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
        PythonVersion,
        HostName,
        OsVersion
    ]
