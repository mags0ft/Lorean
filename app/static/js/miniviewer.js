/**
 * DOM element for the miniview icon
 * @type {HTMLElement}
 */
const MINIVIEW_ICON = document.getElementById("miniview-icon");

/**
 * DOM element for the miniview text
 * @type {HTMLElement}
 */
const MINIVIEW_TEXT = document.getElementById("miniview-text");

/**
 * Updates the miniview display based on backup status data
 * @param {Object} json - The backup status data
 * @param {boolean} json.backup_running - Whether a backup is currently running
 * @param {string} json.progress - The backup progress percentage
 * @returns {void}
 */
function set_miniview(json) {
    if (json["backup_running"]) {
        MINIVIEW_ICON.classList.remove("is-success");
        MINIVIEW_ICON.classList.add("is-warning");

        MINIVIEW_TEXT.innerText = json["progress"] + "%";
    } else {
        MINIVIEW_ICON.classList.add("is-success");
        MINIVIEW_ICON.classList.remove("is-warning");

        MINIVIEW_TEXT.innerText = "No task active";
    }
}

/**
 * Fetches backup status from the API and updates the miniview
 * @returns {void}
 */
function update_miniview() {
    const res = fetch(
        "/backup/monitor-api"
    );

    res.then((response) => {
        response.json().then(set_miniview);
    }).catch((error) => {
        console.error("Failed to update miniview:", error);
    });
}

update_miniview();

setInterval(
    update_miniview, 4000
);