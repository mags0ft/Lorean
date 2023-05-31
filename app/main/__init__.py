from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    g
)
from werkzeug.utils import secure_filename

from ..database import create_database
from ..backupd import start_backup, start_recovery
from ..config import LOGDIR
from uuid import uuid4
from datetime import datetime
import os, json

main = Blueprint("main", __name__)
db = create_database()
pipe, data = None, None

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/settings")
def settings():
    return render_template(
        "settings.html",
        excludes = db["excludes"],
        locations = db["locations"]
    )

@main.route("/settings/set", methods = ["POST"])
def set_settings():
    db["excludes"] = request.form["excludes"].splitlines()
    db["locations"] = request.form["locations"].splitlines()

    return redirect(
        url_for("main.settings")
    )

@main.route("/backup/run", methods = ["POST"])
def run_backup():
    global pipe

    for name, description in {
        "orig": "folder to back up",
        "dest": "destination path for the backup",
        "folder": "name of the backup folder"
    }.items():
        if request.form[name] == "":
            flash(f"Please specify the {description}.", "warning")
            return redirect(url_for("main.new_backup"))

    if pipe != None:
        flash("Already running a backup.", "danger")
        return redirect(url_for("main.new_backup"))

    pipe = start_backup({
        "orig": request.form["orig"],
        "dest": request.form["dest"],
        "folder": request.form["folder"],
        "excludes": db["excludes"]
    })

    return redirect(url_for("main.monitor_backup"))

@main.route("/backup/new")
def new_backup():
    return render_template(
        "new_backup.html",
        dest_folder_name = str(
            datetime.today().strftime('%Y-%m-%d %H-%M') +
            " " + str(uuid4())[:8]
        ),
        locations = db["locations"]
    )

@main.route("/backup/monitor")
def monitor_backup():
    g.monitor = True
    return render_template(
        "monitor_backup.html"   
    )

def refresh_data():
    global data

    if pipe == None: return True

    try:
        if pipe.poll():
            data = pipe.recv()
    except EOFError:
        pass
    except BrokenPipeError:
        return True

    try:
        pipe.send("send data")
        pipe_broken = False
    except BrokenPipeError:
        pipe_broken = True
    return pipe_broken

@main.route("/backup/monitor-api")
def monitor_api():
    global pipe, data

    pipe_broken = refresh_data()

    progress = (
        round((data.current_file_nr + data.skipped) / (
            data.total_file_nr if data.total_file_nr != 0 else 1
        ) * 100, 2) if (
            data != None
        ) else 0
    )

    if pipe_broken:
        pipe = None

    return {
        "backup_running": (pipe != None and not pipe_broken),
        "progress": progress,

        "data": {
            "current_file": data.current_file,
            "current_file_nr": data.current_file_nr + data.skipped,
            "total_file_nr": data.total_file_nr if data.total_file_nr != 0 else 1,
            "skipped": data.skipped,
            "description": data.description
        } if (not pipe_broken) and data != None else {}
    }

@main.route("/logs")
def logs():
    logs_ = sorted([
        l.replace(".log", "") for l in os.listdir(LOGDIR)
    ], reverse = True)
    abs_backup_path = os.path.abspath(LOGDIR)

    return render_template(
        "logs.html",
        logs = logs_,
        abs_backup_path = abs_backup_path
    )

@main.route("/logs/read")
def log_reader():
    name = request.args.get("file")

    with open(
        os.path.join(
            LOGDIR,
            secure_filename(name)
        ), "r"
    ) as f:
        log = f.read()

    return render_template(
        "log_view.html",
        log_name = name,
        log_size = len(log),
        log = log
    )

@main.route("/backup/recover")
def recover_backup():
    return render_template(
        "recover/begin.html",
        locations = db["locations"]
    )

@main.route("/backup/recover/pick", methods = ["POST"])
def recovery_pick():
    if not (
        request.form["dest"] and
        request.form["orig"]
    ):
        flash("Fill out all the fields.", "danger")
        return redirect(url_for("main.recover_backup"))

    backups = next(
        os.walk(request.form["dest"])
    )[1]

    abs_backups = [
        os.path.join(request.form["dest"], b) for b in backups
    ]
    finalized_backups = []

    if "search" in request.form and request.form["search"] == "on":
        search = True
        for idx, el in enumerate(abs_backups):
            try:
                with open(os.path.join(
                    el, ".lorean_meta"
                ), "r") as f:
                    meta = json.load(f)
            except FileNotFoundError:
                flash(f'Skipped "{el}" as no meta information file was found.', "danger")
                continue
            except json.JSONDecodeError:
                flash(f'Skipped "{el}" as the meta information file was corrupted.', "danger")
            
            if meta["folder"] == request.form["orig"]:
                finalized_backups.append(
                    backups[idx]
                )

    else:
        search = False
        finalized_backups = backups

    return render_template(
        "recover/pick.html",
        backups = finalized_backups,
        to_recover = request.form["orig"],
        abs_backup_path = request.form["dest"],
        searched = search
    )

@main.route("/backup/recover/examine", methods = ["POST"])
def examine_backup():
    g.custom_flashes = True


    to_recover = request.form["to-recover"]
    backup = request.form["backup"]
    abs_backup_path = request.form["backup-directory"]
    full_path = os.path.join(
        abs_backup_path, backup
    )

    run_validation(full_path, flash, to_recover)

    return render_template(
        "recover/examine.html",
        backup = backup,

        to_recover = to_recover,
        backup_path = full_path
    )

def run_validation(
        full_path,
        func,
        to_recover = None
    ):
    DISCOURAGE = "It is highly discouraged to continue as it might be extremely risky."

    try:
        with open(os.path.join(
            full_path, ".lorean_meta"
        ), "r") as f:
            meta = json.load(f)

        func(f"Meta information file seems to be intact.", "success")
    except FileNotFoundError:
        func(f'''CRITICAL: no backup meta file has been found. This probably means that
        the picked folder is corrupted or not even a valid backup made with Lorean. 
        {DISCOURAGE}''', "danger")
        meta = None
    
    except json.JSONDecodeError:
        func(f'''CRITICAL: the backup's meta information failed to load. This could mean your
        backup is encrypted or corrupted. {DISCOURAGE}''', "danger")
        meta = None

    if meta != None:
        if meta["lock"]:
            func('''CRITICAL: according to the backup meta file, the backup has not been completed.
            Therefore, it might be missing many important files.''', "danger")
        else:
            func("The backup seems to have been completed.", "success")

        if (meta["folder"] != to_recover) and (not to_recover == None):
            func(f'''WARNING: this backup seems to contain files intended for another directory.
            Maybe you renamed your folder or picked a wrong backup. Please double-check everything
            before you continue!''', "danger")
        else:
            func("Folders of recovery and backup match.", "success")

        total_files = sum(
            len(_files) for _, _, _files in os.walk(
                full_path
            )
        ) - 1 # for the meta file
        if meta["files"] > total_files:
            func(
                f'''WARNING: The backup is missing {meta['files'] - total_files} file(s) in it and
                is therefore incomplete.''',
                "danger"
            )
        elif meta["files"] < total_files:
            func(
                f'''WARNING: The backup contains {total_files - meta['files']} file(s) more than
                originally expected according to the meta information file. It seems like it has
                been tampered with.''',
                "danger"
            )
        else:
            func("Could validate that the backup is not missing files.", "success")

    else:
        func("Skipped all security checks due to missing meta file.", "danger")

@main.route("/backup/recover/run", methods = ["POST"])
def run_recovery():
    global pipe

    if pipe != None:
        flash("Already running a task.", "danger")
        return redirect(url_for("main.monitor_backup"))

    pipe = start_recovery({
        "orig": request.form["backup-path"],
        "dest": request.form["to-recover"]
    })

    return redirect(url_for("main.monitor_backup"))

@main.route("/manage", methods = ["GET", "POST"])
def manage_backups():
    if request.method.upper() == "GET":
        return render_template(
            "manage/begin.html",
            locations = db["locations"]
        )
    
    directory = request.form["dest"]

    def dir_size_mb(dir_):
        total_size = 0

        for dir_path, _, filenames in os.walk(dir_):
            for file in filenames:
                file_path = os.path.join(dir_path, file)
                if os.path.islink(file_path): return

                total_size += os.path.getsize(file_path)

        return round(total_size / (1024 ** 2), 2)
    
    backups = {}
    for b in os.listdir(directory):
        p = os.path.join(directory, b)
        if not os.path.isdir(p): return

        backups[b] = {
            "size": 0,
            "errors": []
        }

        run_validation(
            p,
            lambda err, status: backups[b]["errors"].append(err) if status != "success" else 0
        )

        backups[b]["size"] = dir_size_mb(p)
    
    return render_template(
        "manage/view.html",
        backups = backups,
        path = directory
    )