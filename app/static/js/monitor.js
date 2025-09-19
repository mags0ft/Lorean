/**
 * Progress bar element for displaying backup progress
 * @type {HTMLElement}
 */
const PROGRESS_BAR = document.getElementById("progress-bar");

/**
 * Interval ID for the monitoring update cycle
 * @type {number}
 */
let interval = 0;

/**
 * Updates the monitor UI based on backup status data
 * @param {Object} json - The backup status data
 * @param {boolean} json.backup_running - Whether a backup is currently running
 * @param {Object} json.data - Backup progress data
 * @param {string} json.data.description - Current backup description/status
 * @param {number} json.data.total_file_nr - Total number of files to backup
 * @param {number} json.data.current_file_nr - Current file number being processed
 */
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

    for (const key in json["data"]) {
        if (json["data"].hasOwnProperty(key)) {
            document.getElementById(key).innerText = json["data"][key];
        }
    }

    PROGRESS_BAR.max = json["data"]["total_file_nr"];
    const cur_file_nr = json["data"]["current_file_nr"];
    if (cur_file_nr != 0) {
        PROGRESS_BAR.value = cur_file_nr;
    } else {
        PROGRESS_BAR.value = "";
    }
}

/**
 * Fetches backup status from the server and updates the monitor
 * Makes an HTTP request to the backup monitor API endpoint
 */
function update_monitor() {
    const res = fetch(
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