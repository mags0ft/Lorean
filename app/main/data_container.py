"""
Module containing data classes used in the application.
Currently, only the Progress class is defined here. It tracks the progress of
a job, including the current file being processed, the number of files
processed, the total number of files, and any skipped files.
"""

from dataclasses import dataclass


@dataclass
class Progress:
    """
    Class to keep track of the current job progress.
    """

    current_file: str = ""
    current_file_nr: int = 0
    total_file_nr: int = 0
    skipped: int = 0
    description: str = "Copying files to target directory..."
