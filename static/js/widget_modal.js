// Dashboard Widget Edit Modal interactions

document.addEventListener("DOMContentLoaded", function () {
    const editForm = document.getElementById("edit-widget-form");
    const widgetIdInput = document.getElementById("edit-widget-id");
    const widgetNameInput = document.getElementById("edit-widget-name");
    const widgetTypeSelect = document.getElementById("edit-widget-type");
    const widgetWidthSelect = document.getElementById("edit-widget-width");
    const widgetSortInput = document.getElementById("edit-widget-sort");

    // Click triggers
    document.querySelectorAll(".edit-widget-trigger").forEach(trigger => {
        trigger.addEventListener("click", function (e) {
            e.preventDefault();
            const widgetId = this.getAttribute("data-id");
            
            // Clear errors
            clearFormErrors();

            // Fetch widget details via GET API
            fetch(`/dashboard/widget/${widgetId}/`)
                .then(response => {
                    if (!response.ok) throw new Error("Could not fetch widget details.");
                    return response.json();
                })
                .then(data => {
                    widgetIdInput.value = data.id;
                    widgetNameInput.value = data.widget_name;
                    widgetTypeSelect.value = data.widget_type;
                    widgetWidthSelect.value = data.width;
                    widgetSortInput.value = data.sort_order;

                    const modalEl = document.getElementById("editWidgetModal");
                    const inst = bootstrap.Modal.getOrCreateInstance(modalEl);
                    inst.show();
                })
                .catch(err => {
                    alert(err.message || "An error occurred while loading settings.");
                });
        });
    });

    // Form submission
    editForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const widgetId = widgetIdInput.value;
        const formData = new FormData(editForm);

        clearFormErrors();

        // Save details via POST API
        fetch(`/dashboard/widget/${widgetId}/update/`, {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": getCsrfToken()
            }
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    if (data.errors) {
                        displayFormErrors(data.errors);
                    }
                    throw new Error("Validation failed");
                });
            }
            return response.json();
        })
        .then(data => {
            // Success! Update DOM width and labels in real-time
            const widgetContainer = document.getElementById(`widget-container-${widgetId}`);
            if (widgetContainer) {
                // Update Name
                const titleEl = document.getElementById(`widget-title-${widgetId}`);
                if (titleEl) titleEl.textContent = data.widget.widget_name;

                // Update width class
                widgetContainer.className = "widget-col col-12"; // Reset
                const widthVal = parseInt(data.widget.width);
                let colClass = "col-lg-6";
                if (widthVal === 25) colClass = "col-lg-3";
                else if (widthVal === 33) colClass = "col-lg-4";
                else if (widthVal === 50) colClass = "col-lg-6";
                else if (widthVal === 66) colClass = "col-lg-8";
                else if (widthVal === 75) colClass = "col-lg-9";
                else if (widthVal === 100) colClass = "col-lg-12";
                widgetContainer.classList.add(colClass);

                // Update sort attribute
                widgetContainer.setAttribute("data-sort", data.widget.sort_order);

                // Re-sort widget layout order inside parent grid
                reorderWidgets();
            }

            const modalEl = document.getElementById("editWidgetModal");
            const inst = bootstrap.Modal.getOrCreateInstance(modalEl);
            inst.hide();
            
            // Show inline temporary success notice
            const notice = document.createElement("div");
            notice.className = "alert alert-success position-fixed bottom-0 end-0 m-3 shadow";
            notice.style.zIndex = "9999";
            notice.textContent = data.message;
            document.body.appendChild(notice);
            setTimeout(() => notice.remove(), 3000);
        })
        .catch(err => {
            console.error("Save failed:", err);
        });
    });

    // Helper functions
    function clearFormErrors() {
        document.getElementById("error-widget-name").textContent = "";
        document.getElementById("error-widget-type").textContent = "";
        document.getElementById("error-widget-width").textContent = "";
        document.getElementById("error-widget-sort").textContent = "";
    }

    function displayFormErrors(errors) {
        if (errors.widget_name) {
            document.getElementById("error-widget-name").textContent = errors.widget_name[0].message;
        }
        if (errors.widget_type) {
            document.getElementById("error-widget-type").textContent = errors.widget_type[0].message;
        }
        if (errors.width) {
            document.getElementById("error-widget-width").textContent = errors.width[0].message;
        }
        if (errors.sort_order) {
            document.getElementById("error-widget-sort").textContent = errors.sort_order[0].message;
        }
    }

    function reorderWidgets() {
        const container = document.getElementById("dashboard-widgets-container");
        if (!container) return;

        const cols = Array.from(container.children);
        cols.sort((a, b) => {
            const sortA = parseInt(a.getAttribute("data-sort")) || 0;
            const sortB = parseInt(b.getAttribute("data-sort")) || 0;
            return sortA - sortB;
        });

        // Append sorted elements
        cols.forEach(col => container.appendChild(col));
    }

    function getCsrfToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        return cookieValue || "";
    }
});
