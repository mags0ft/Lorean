from multiprocessing import Process, Pipe
from ...app.main.data_container import Progress

from os import walk, mkdir, path
from shutil import copy
import re

def refresh_status(
    pipe,
    current_file = "",
    current_file_nr = 0,
    total_file_nr = 0,
    skipped = 0,
    description = ""
):
    pipe.send(Progress(
        current_file,
        current_file_nr,
        total_file_nr,
        skipped,
        description
    ))

def backup(p, config: dict):
    refresh_status(p, description = "initializing backup...")

    originating_path = config["orig"]
    destination_path = config["dest"]
    destination_folder = config["folder"]
    regexs = config["excludes"]
    finalized_regexs = []

    for idx, regex in enumerate(regexs):
        if not regex:
            regexs.remove(regex)
            continue
        
        try:
            finalized_regexs.append(re.compile(regex))
        except re.error:
            refresh_status(p, description = f"error: invalid exclude regex at line {idx + 1}: '{regex}'")
            return 1

    total_files = sum(
        len(_files) for _, _, _files in walk(
            originating_path
        )
    )

    ###

    file_nr = 1
    skipped = 0
    mkdir(
        path.join(destination_path, destination_folder)
    )

    for path_, dirs, files in walk(originating_path):
        rel_path = path_[len(originating_path)+1:]

        for dir in dirs:
            mkdir(path.join(destination_path, destination_folder, rel_path, dir))

        for file in files:
            if any(regex.search(path.join(rel_path, file)) != None for regex in finalized_regexs):
                skipped += 1
                continue

            elif p.poll():
                refresh_status(
                    p,
                    current_file = path.join(rel_path, file),
                    current_file_nr = file_nr,
                    total_file_nr = total_files,
                    skipped = skipped,
                    description = "Copying files..."
                )
                p.recv()

            copy(
                path.join(path_, file),
                path.join(destination_path, destination_folder, rel_path, file)
            )

            file_nr += 1

    ###

    refresh_status(p, description = "finished.")

def start_backup(config):
    parentc, childc = Pipe()

    backup_process = Process(
        target = backup,
        args = (childc, config, )
    )
    backup_process.name = "Lorean backup process daemon"

    backup_process.daemon = True
    backup_process.start()

    return parentc