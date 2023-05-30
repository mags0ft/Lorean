let INPUT = document.getElementById("path-input");
let FORM = document.getElementById("recover-form");

function set_backup(path) {
    INPUT.value = path;
    FORM.submit();
}