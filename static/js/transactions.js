// Transactions Module Interactions

document.addEventListener("DOMContentLoaded", function () {
    const mainForm = document.getElementById("transaction-main-form");
    const saveBtn = document.getElementById("btn-save-transaction");

    // 1. Disable save button on form submission
    if (mainForm && saveBtn) {
        mainForm.addEventListener("submit", function () {
            saveBtn.disabled = true;
            saveBtn.innerHTML = `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Saving...`;
        });
    }

    // 2. Drag and Drop for Attachments
    const dropZone = document.getElementById("import-drop-zone");
    const fileInput = document.getElementById("attachment-file-input");
    const dropText = document.getElementById("import-drop-text");

    if (dropZone && fileInput) {
        dropZone.addEventListener("click", () => fileInput.click());

        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                dropZone.classList.add('dragover');
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                dropZone.classList.remove('dragover');
            }, false);
        });

        dropZone.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            const files = dt.files;
            if (files.length > 0) {
                fileInput.files = files;
                updateDropText(files[0].name);
            }
        });

        fileInput.addEventListener('change', () => {
            if (fileInput.files.length > 0) {
                updateDropText(fileInput.files[0].name);
            }
        });

        function updateDropText(name) {
            if (dropText) {
                dropText.innerHTML = `<i class="bi bi-file-earmark-check text-success fs-2 d-block mb-2"></i> <strong>Selected:</strong> ${name}`;
            }
        }
    }
});
