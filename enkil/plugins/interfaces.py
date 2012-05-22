#import socket

from enkil.log import getLogger
from enkil.main import InfoClass

log = getLogger(__name__)


class Interfaces(InfoClass):
    DEPENDENCIES = None

    def get(self, info):
        return {}


def getHandlers(base_info):
    return [
        Interfaces,
    ]
