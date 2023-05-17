class Progress:
    current_file = ""

    current_file_nr = 0
    total_file_nr = 0

    description = "Copying files to target directory..."

    def __init__(self, current_file, current_file_nr, total_file_nr, description):
        (
            self.current_file,
            self.current_file_nr,
            self.total_file_nr,
            self.description
        ) = (
            current_file,
            current_file_nr,
            total_file_nr,
            description
        )