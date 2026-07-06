// Onboarding Wizard & Loading Page interactions

document.addEventListener("DOMContentLoaded", function () {
    // 1. Loading Page Auto Redirect
    const loadingScreen = document.getElementById("loading-screen-trigger");
    if (loadingScreen) {
        setTimeout(function () {
            window.location.href = "/company/profile/";
        }, 3000); // 3 seconds timeout
    }

    // 2. Drag & Drop File Upload Handler
    const dropZone = document.getElementById("logo-drop-zone");
    const fileInput = document.getElementById("logo-file-input");
    const dropZoneText = document.getElementById("drop-zone-text");

    if (dropZone && fileInput) {
        // Clicking on zone opens file browser
        dropZone.addEventListener("click", () => fileInput.click());

        // Highlight drop zone when item dragged over it
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

        // Handle dropped files
        dropZone.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            const files = dt.files;
            if (files.length > 0) {
                fileInput.files = files;
                updateFileNameDisplay(files[0].name);
            }
        });

        // Handle file selected from input
        fileInput.addEventListener('change', () => {
            if (fileInput.files.length > 0) {
                updateFileNameDisplay(fileInput.files[0].name);
            }
        });

        function updateFileNameDisplay(name) {
            if (dropZoneText) {
                dropZoneText.innerHTML = `<i class="bi bi-file-earmark-image text-success fs-3 d-block mb-1"></i> <strong>Selected:</strong> ${name}`;
            }
        }
    }
});
