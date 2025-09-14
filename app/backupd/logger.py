"""
Logging setup for the backup and recovery processes.
Manages log formatting and file handling.
"""

import logging


def create_logger(name, filepath):
    """
    Creates a logger object for the backup and recovery processes.
    Logs are written to the specified file with a detailed format.
    Returns the configured logger instance.
    """

    l = logging.getLogger(name)
    l.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s.%(msecs)02d %(levelname)s: %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )

    handler = logging.FileHandler(filepath)

    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)

    l.addHandler(handler)

    return l
