// Reconciliation Module Interactions

document.addEventListener("DOMContentLoaded", function () {
    const btnLoad = document.getElementById("btn-load-transactions");
    const accountSelect = document.getElementById("id_account");
    const startDateInput = document.getElementById("id_start_date");
    const endDateInput = document.getElementById("id_end_date");
    const tableBody = document.getElementById("reconciliation-table-body");

    if (btnLoad) {
        btnLoad.addEventListener("click", function () {
            const account = accountSelect.value;
            const startDate = startDateInput.value;
            const endDate = endDateInput.value;

            if (!account || !startDate || !endDate) {
                alert("Please fill in Start Date, End Date, and Account selection before loading transactions.");
                return;
            }

            btnLoad.disabled = true;
            btnLoad.textContent = "Loading...";

            // Fetch via AJAX query
            fetch(`/reconciliation/load-transactions/?account=${account}&start_date=${startDate}&end_date=${endDate}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error("Network response was not ok");
                    }
                    return response.text();
                })
                .then(html => {
                    tableBody.innerHTML = html;
                })
                .catch(error => {
                    console.error("Error loading transactions:", error);
                    tableBody.innerHTML = `<tr><td colspan="6" class="text-center text-danger">Failed to load transactions. Please try again.</td></tr>`;
                })
                .finally(() => {
                    btnLoad.disabled = false;
                    btnLoad.textContent = "Transactions";
                });
        });
    }

    // Modal delete confirms
    window.triggerDeleteModal = function (recId, recLabel) {
        const labelEl = document.getElementById("delete-rec-label");
        const btnEl = document.getElementById("delete-confirm-btn");
        if (labelEl && btnEl) {
            labelEl.textContent = recLabel;
            btnEl.href = `/reconciliation/${recId}/delete/`;
            const modal = new bootstrap.Modal(document.getElementById("deleteConfirmationModal"));
            modal.show();
        }
    };
});
