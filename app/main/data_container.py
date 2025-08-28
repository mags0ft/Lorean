"""
Module for any data containing classes.
TODO: consider migration to dataclasses.
"""

class Progress:
    """
    Class to keep track of the current job progress.
    """
    
    current_file = ""

    current_file_nr = 0
    total_file_nr = 0
    skipped = 0

    description = "Copying files to target directory..."

    def __init__(self, current_file, current_file_nr, total_file_nr, skipped, description):
        """
        Initializes the progress class.
        """
        
        (
            self.current_file,
            self.current_file_nr,
            self.total_file_nr,
            self.skipped,
            self.description
        ) = (
            current_file,
            current_file_nr,
            total_file_nr,
            skipped,
            description
        )
