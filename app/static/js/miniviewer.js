let MINIVIEW_ICON = document.getElementById("miniview-icon");
let MINIVIEW_TEXT = document.getElementById("miniview-text");

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

function update_miniview() {
    var res = fetch(
        "/backup/monitor-api"
    );

    res.then((response) => {
        response.json().then(set_miniview);
    });
}

update_miniview();
setInterval(
    update_miniview, 4000
);