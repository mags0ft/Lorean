let PROGRESS_BAR = document.getElementById("progress-bar");
let interval = 0;

function set_monitor(json) {
    if (!json["backup_running"]) {
        document.getElementById("description").innerText =
        "All backup tasks seem to have finished. There is no backup running anymore.";
        PROGRESS_BAR.classList.add("is-success");
        PROGRESS_BAR.classList.remove("is-primary");
        PROGRESS_BAR.value = 1;
        PROGRESS_BAR.max = 1;

        return;
    } else {
        if (json["data"]["description"].startsWith("error")) {
            PROGRESS_BAR.classList.remove("is-success");
            PROGRESS_BAR.classList.remove("is-primary");
            PROGRESS_BAR.classList.add("is-danger");

            document.getElementById("description").classList.add("has-text-danger");
            document.getElementById("description").innerText = json["data"]["description"];
            
            clearInterval(interval)
            return;
        }
        PROGRESS_BAR.classList.add("is-primary");
        PROGRESS_BAR.classList.remove("is-success");
        document.getElementById("description").classList.remove("has-text-danger");
    }

    for (key in json["data"]) {
        document.getElementById(key).innerText = json["data"][key];
    }

    PROGRESS_BAR.max = json["data"]["total_file_nr"];
    cur_file_nr = json["data"]["current_file_nr"];
    if (cur_file_nr != 0) {
        PROGRESS_BAR.value = cur_file_nr;
    } else {
        PROGRESS_BAR.value = "";
    }
}

function update_monitor() {
    var res = fetch(
        "/backup/monitor-api"
    );

    res.then((response) => {
        response.json().then(set_monitor);
    });
}

interval = setInterval(
    update_monitor, REFRESH_CYCLE
);
update_monitor();