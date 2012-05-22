from __future__ import absolute_import

import time
from datetime import datetime

from enkil.log import getLogger
from enkil.main import InfoClass

log = getLogger(__name__)


class CurrTime(InfoClass):
    DEPENDENCIES = None

    def get(self, info):
        now = datetime.now()
        utcnow = datetime.utcnow()
        return {
            "localtime": now.ctime(),
            "gmtime": utcnow.ctime(),
            "localisotime": now.isoformat(),
            "gmisotime": utcnow.isoformat(),

            "time": now.strftime("%H%M%S"),
            "date": now.strftime("%Y%m%d"),
        }


class TimeZone(InfoClass):
    DEPENDENCIES = None

    def get(self, info):
        return {
            "dst": True if time.daylight == 1 else False,
            "tzname": time.tzname[1] if time.daylight != 0 else time.tzname[0],
            "tzoffset": time.altzone if time.daylight != 0 else 0,
        }


def getHandlers(info):
    return [
        CurrTime,
        TimeZone
    ]
