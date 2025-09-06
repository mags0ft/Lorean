let input = document.getElementById("path-input");
let form = document.getElementById("recover-form");

function set_backup(path) {
    input.value = path;
    form.submit();
}
