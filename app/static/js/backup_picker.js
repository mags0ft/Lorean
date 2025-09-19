/**
 * The backup destination path input element
 * @type {HTMLElement}
 */
const INPUT = document.getElementById("backup-dest-path");

/**
 * Sets the value of the backup destination path input field
 * @param {string} path - The file path to set as the input value
 */
function set_path(path) {
    INPUT.value = path;
}