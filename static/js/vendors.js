// Vendors Module Interactions

document.addEventListener("DOMContentLoaded", function () {
    const contactTableBody = document.getElementById("contact-persons-body");
    const btnAddContact = document.getElementById("btn-add-contact-row");

    // 1. Add Contact Person Row dynamically
    if (btnAddContact && contactTableBody) {
        btnAddContact.addEventListener("click", function () {
            const newRow = document.createElement("tr");
            newRow.innerHTML = `
                <td>
                    <input type="text" name="contact_name[]" class="form-control" placeholder="Name" required>
                </td>
                <td>
                    <input type="email" name="contact_email[]" class="form-control" placeholder="Email">
                </td>
                <td>
                    <input type="text" name="contact_phone[]" class="form-control" placeholder="Phone">
                </td>
                <td class="text-center">
                    <button type="button" class="btn btn-outline-danger btn-sm btn-delete-contact"><i class="bi bi-trash"></i></button>
                </td>
            `;
            contactTableBody.appendChild(newRow);
            bindDeleteRowButton(newRow.querySelector(".btn-delete-contact"), newRow);
        });
    }

    function bindDeleteRowButton(button, row) {
        if (button && row) {
            button.addEventListener("click", function () {
                row.remove();
            });
        }
    }

    // Bind delete action for any initial rows
    if (contactTableBody) {
        contactTableBody.querySelectorAll("tr").forEach(row => {
            const deleteBtn = row.querySelector(".btn-delete-contact");
            if (deleteBtn) {
                bindDeleteRowButton(deleteBtn, row);
            }
        });
    }

    // 2. Logo image preview
    const logoInput = document.getElementById("logo-file-input");
    const logoPreviewContainer = document.getElementById("logo-preview-container");
    const logoPreviewImage = document.getElementById("logo-preview-image");

    if (logoInput && logoPreviewContainer && logoPreviewImage) {
        logoInput.addEventListener("change", function () {
            const file = logoInput.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    logoPreviewImage.src = e.target.result;
                    logoPreviewContainer.classList.remove("d-none");
                };
                reader.readAsDataURL(file);
            } else {
                logoPreviewImage.src = "#";
                logoPreviewContainer.classList.add("d-none");
            }
        });
    }

    // 3. Drag and Drop for Excel Imports
    const dropZone = document.getElementById("import-drop-zone");
    const fileInput = document.getElementById("import-file-input");
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
                dropText.innerHTML = `<i class="bi bi-file-earmark-spreadsheet text-success fs-2 d-block mb-2"></i> <strong>Selected:</strong> ${name}`;
            }
        }
    }
});
