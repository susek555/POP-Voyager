import logging

RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

COLORS = {"WARNING": YELLOW, "INFO": GREEN, "DEBUG": BLUE, "CRITICAL": RED, "ERROR": RED}


class ColoredFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        levelname = record.levelname
        color = COLOR_SEQ % (30 + COLORS.get(levelname, 0))
        record.levelname = f"{color}{levelname}{RESET_SEQ}"
        return super().format(record)


def setup_logger(level: int | str) -> None:
    logger = logging.getLogger()
    logger.setLevel(level)
    handler = logging.StreamHandler()
    formatter = ColoredFormatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
