// Accounts module interactions

document.addEventListener("DOMContentLoaded", function () {
    // Confirm delete trigger handles
    window.triggerDeleteModal = function (accountId, accountName) {
        const deleteNameEl = document.getElementById("delete-account-name");
        const deleteBtnEl = document.getElementById("delete-confirm-btn");
        if (deleteNameEl && deleteBtnEl) {
            deleteNameEl.textContent = accountName;
            deleteBtnEl.href = `/banking/accounts/${accountId}/delete/`;
            const modal = new bootstrap.Modal(document.getElementById("deleteConfirmationModal"));
            modal.show();
        }
    };
});
