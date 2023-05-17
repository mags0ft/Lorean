from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    make_response,
    request
)

from ...app.database import create_database
from ...app.backupd import start_backup
from uuid import uuid4
from datetime import datetime

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
        excludes = db["excludes"]
    )

@main.route("/settings/set", methods = ["POST"])
def set_settings():
    db["excludes"] = request.form["excludes"].splitlines()

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

    if pipe != None or (pipe != None and not pipe.closed):
        flash("Already running a backup.", "danger")
        return redirect(url_for("main.new_backup"))

    pipe = start_backup({
        "orig": request.form["orig"],
        "dest": request.form["dest"],
        "folder": request.form["folder"],
        "excludes": db["excludes"]
    })

    flash("Backup started. This can take a while.", "success")

    return redirect(url_for("main.monitor_backup"))

@main.route("/backup/new")
def new_backup():
    return render_template(
        "new_backup.html",
        dest_folder_name = str(
            datetime.today().strftime('%Y-%m-%d %H-%M') +
            " " + str(uuid4())[:8]
        )
    )

@main.route("/backup/monitor")
def monitor_backup():
    global data, pipe

    if pipe == None or pipe.closed:
        flash("All backup tasks have been finished!", "success")
        return redirect(url_for("main.index"))

    try:
        data = pipe.recv()
    except EOFError:
        pass

    try:
        pipe.send("send data")
        pipe_broken = False
    except BrokenPipeError:
        pipe_broken = True

    if data.description == "finished" or pipe_broken:
        flash("The backup has been completed.", "success")
        pipe.close()
        pipe = None

        return redirect(url_for("main.index"))
    
    elif data.description.startswith("error"):
        flash(data.description, "danger")

        return redirect(url_for("main.index"))

    r = make_response(   
        render_template(
            "monitor_backup.html",

            current_file = data.current_file,
            current_file_nr = data.current_file_nr,
            total_file_nr = data.total_file_nr if data.total_file_nr != 0 else 1,
            skipped = data.skipped,
            description = data.description
        )
    )
    r.headers["Refresh"] = "1"
    return r