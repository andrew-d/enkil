import sys
import time
import logging

try:
    import curses
except ImportError:
    curses = None


try:
    import colorama
    colorama.init()
except ImportError:
    colorama = None


class CustomFormatter(logging.Formatter):
    """
    This class implements a custom logging formatter that outputs in color, on
    both *nix and Windows systems.  It gracefully degrades if no color-handling
    modules are available.  For simplicity, the format string is hard-coded in
    the format() method of the class, and thus the `fmt` and `datefmt`
    arguments are ignored.
    """

    def __init__(self, *args, **kwargs):
        super(CustomFormatter, self).__init__(*args, **kwargs)

        # Do we have color?
        if curses is not None:
            self._have_color = curses.can_change_color()
        elif colorama is not None:
            self._have_color = True
        else:
            self._have_color = False

        # Debug level --> ANSI escape code mapping
        self._colors = {
            logging.DEBUG:      '\x1b[34m',     # Blue
            logging.INFO:       '\x1b[32m',     # Green
            logging.WARNING:    '\x1b[33m',     # Yellow
            logging.ERROR:      '\x1b[31m',     # Red
        }
        self._nocolor = '\x1b[39m'

        # Set the converter to log everything in GMT time.
        self.converter = time.gmtime

    def format(self, record):
        try:
            record.message = record.getMessage()
        except Exception:
            record.message = "Exception while getting message: %r" % (sys.exc_info()[1])

        # Get the time.
        record.asctime = self.formatTime(record)

        # Build our prefix with the color.
        prefix = '[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d]'
        if self._have_color:
            color = self._colors.get(record.levelno, self._nocolor)
            prefix = color + prefix + self._nocolor

        # Make our format string, and then format it.
        format_string = prefix + " " + "%(message)s"
        formatted = format_string % record.__dict__

        # Format the exeception information, if it exists.
        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)

        # If we have exception text, append it to our message.
        if record.exc_text:
            formatted = formatted.rstrip() + "\n" + record.exc_text

        # Replace all newlines with indented newlines.
        return formatted.replace("\n", "\n    ")

    def formatTime(self, record, datefmt=None):
        return time.strftime("%Y-%m-%d %H:%M:%S", self.converter(record.created))


def getLogger(id, minLevel=logging.DEBUG):
    logger = logging.getLogger(id)
    logger.setLevel(minLevel)

    # Create and attach handler(s)
    handler = logging.StreamHandler()
    logger.addHandler(handler)

    # Create and attach formatter to the handler
    fmt = CustomFormatter()
    handler.setFormatter(fmt)

    return logger
