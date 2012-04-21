from .log import getLogger

log = getLogger(__name__)


def main():
    log.debug("main function started")

    # stuff

    log.debug("main function ending")


if __name__ == "__main__":
    main()
