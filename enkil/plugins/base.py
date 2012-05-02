"""
This plugin is the "base" plugin - it provides the most basic information
needed to bootstrap other plugins.  Specifically, it provides:

 - Python version
 - Python executable
 - Operating system and version
 - Host name and FQDN
 - Time

"""

import sys
import socket
import platform

from enkil.log import getLogger
from enkil.main import InfoClass

log = getLogger(__name__)


class PythonInfo(InfoClass):
    DEPENDENCIES = None

    def get(self, info):
        return {
            "python_version": platform.python_version(),
            "python_executable": sys.executable
        }


class HostName(InfoClass):
    DEPENDENCIES = None

    def get(self, info):
        return {
            "hostname": socket.gethostname(),
            "fqdn": socket.getfqdn(),
        }


class OsVersion(InfoClass):
    DEPENDENCIES = None

    def get(self, info):
        return {
            "platform": {
                "name": platform.system().lower(),
                "release": platform.release().lower(),
                "version": platform.version().lower(),
                "fullname": platform.platform(),
                "endian": sys.byteorder,
            }
        }


def getHandlers(base_info):
    log.debug("base getHandlers() called")

    return [
        PythonInfo,
        HostName,
        OsVersion,
    ]
