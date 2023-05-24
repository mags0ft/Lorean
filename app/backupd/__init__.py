from multiprocessing import Process, Pipe
from ...app.main.data_container import Progress
from ...app.backupd.logger import create_logger
from ...app.config import LOGDIR, LOG_SKIPS, LOG_COPY
from uuid import uuid4

from os import walk, mkdir, path
from shutil import copy
from time import sleep
from traceback import format_exc
from logging import Logger
import re, json, datetime

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

def write_meta(
        destination_path,
        destination_folder,
        originating_path,
        created = "",
        finished = "",
        files = 0,
        lock = False
    ):
    with open(path.join(destination_path, destination_folder, ".lorean_meta"), "w") as f:
        json.dump({
            "created": created,
            "finished": finished, 
            "files": files,
            "folder": originating_path,
            "lock": lock
        }, f)

def get_current_date():
    return datetime.datetime.now().strftime('%Y-%m-%d %H-%M')

def backup(p, logger: Logger, config: dict):

    refresh_status(p, description = "initializing backup...")
    logger.info("Initializing backup.")

    originating_path = config["orig"]
    destination_path = config["dest"]
    destination_folder = config["folder"]
    regexes = config["excludes"]
    finalized_regexes = []

    logger.info(f'''Backup config:
    originating path:       {originating_path}
    destination path:       {destination_path}
    destination folder:     {destination_folder}
    exclude regex amount:   {len(regexes)}''')

    logger.debug("Compiling/validating regexes")
    for idx, regex in enumerate(regexes):
        if not regex:
            regexes.remove(regex)
            continue
        
        try:
            finalized_regexes.append(re.compile(regex))
        except re.error:
            error_msg = f"error: invalid exclude regex at line {idx + 1}: '{regex}'"
            logger.fatal(error_msg)

            refresh_status(p, description = error_msg)
            sleep(5)

            return 1

    logger.debug("Counting amount of files")
    total_files = sum(
        len(_files) for _, _, _files in walk(
            originating_path
        )
    )
    logger.info(f"{total_files} counted (ignoring possibly skipped files)")

    ###

    backup_begin = get_current_date()

    file_nr = 1
    skipped = 0

    logger.info("Creating backup directory")
    mkdir(
        path.join(destination_path, destination_folder)
    )

    logger.info("Writing meta file")
    write_meta(
        destination_path,
        destination_folder,
        originating_path,
        backup_begin,
        lock = True
    )

    logger.info("Copying files")
    if LOG_COPY or LOG_SKIPS:
        logger.info("s = skipped; c = copied")
    for path_, dirs, files in walk(originating_path):
        rel_path = path_[len(originating_path)+1:]

        for dir in dirs:
            mkdir(path.join(destination_path, destination_folder, rel_path, dir))

        for file in files:
            fp = path.join(rel_path, file)
            if p.poll():
                refresh_status(
                    p,
                    current_file = fp,
                    current_file_nr = file_nr,
                    total_file_nr = total_files,
                    skipped = skipped,
                    description = "Copying files..."
                )
                p.recv()
            
            elif any(regex.search(fp) != None for regex in finalized_regexes):
                skipped += 1
                if LOG_SKIPS:
                    logger.info(f"s {fp}")
                continue

            if LOG_COPY:
                logger.info(f"c {fp}")
            copy(
                path.join(path_, file),
                path.join(destination_path, destination_folder, rel_path, file)
            )

            file_nr += 1

    ###

    logger.info("Finalizing meta file")

    write_meta(
        destination_path,
        destination_folder,
        originating_path,
        backup_begin,
        get_current_date(),
        total_files - skipped,
        lock = False
    )

    refresh_status(p, description = "finished.")

    logger.info(f"{total_files - skipped} copied, {skipped} skipped.")
    logger.info("Backup finished, process exiting.")

    return 0

def backup_wrapper(childc, config):
    logger = create_logger(
        f"backup {get_current_date()}", path.join(
            LOGDIR, f"{get_current_date().replace(' ', '_')}_{str(uuid4())[:8]}.log"
        )
    )

    try:
        backup(childc, logger, config)
    except Exception as e:
        exc_info = format_exc()

        logger.fatal(f'''
Fatal exception. Backup stopped. Process will exit soon.
{exc_info}''')

        refresh_status(childc, description = f"error: {e}")
        sleep(5)

        raise e

def start_backup(config):
    parentc, childc = Pipe()

    backup_process = Process(
        target = backup_wrapper,
        args = (childc, config, )
    )
    backup_process.name = "Lorean backup process"

    backup_process.daemon = True
    backup_process.start()

    return parentc