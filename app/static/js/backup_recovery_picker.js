/**
 * Input element for the backup path
 * @type {HTMLInputElement}
 */
const pathInput = document.getElementById("path-input");

/**
 * Form element for backup recovery
 * @type {HTMLFormElement}
 */
const recoveryForm = document.getElementById("recover-form");

/**
 * Sets the backup path and submits the recovery form
 * @param {string} path - The backup path to set
 * @returns {void}
 */
function set_backup(path) {
    pathInput.value = path;
    recoveryForm.submit();
}
