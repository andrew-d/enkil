from __future__ import absolute_import

import time

from enkil.log import getLogger
from enkil.main import InfoClass

log = getLogger(__name__)


class CurrTime(InfoClass):
    DEPENDENCIES = None

    def get(self, info):
        return {
            "localtime": time.time(),
            "dst": True if time.daylight == 1 else False,
            "gmtime": time.mktime(time.gmtime()),
            "ctime": time.ctime(),
        }


def getHandlers(info):
    return [
        CurrTime
    ]
