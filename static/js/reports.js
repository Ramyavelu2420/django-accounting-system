// Reports Module Interactions

document.addEventListener("DOMContentLoaded", function () {
    // 1. AJAX Pin / Unpin report handler
    window.togglePinReport = function (reportId, pinEl) {
        const isPinned = pinEl.classList.contains("active") || pinEl.querySelector("i").classList.contains("bi-pin-fill");
        const url = isPinned ? `/reports/unpin/${reportId}/` : `/reports/pin/${reportId}/`;

        fetch(url, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCsrfToken(),
                "Content-Type": "application/json"
            }
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => { throw new Error(data.message || "Failed action"); });
            }
            return response.json();
        })
        .then(data => {
            // Reload page to reflect updated pins and counts cleanly
            window.location.reload();
        })
        .catch(err => {
            alert(err.message || "An error occurred while updating pin status.");
        });
    };

    // Helper to get CSRF Token
    function getCsrfToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        return cookieValue || "";
    }

    // 2. Client-side Category Filter button handles
    const filterButtons = document.querySelectorAll(".reports-filter-btn");
    const categoriesSections = document.querySelectorAll(".reports-category-section");

    filterButtons.forEach(btn => {
        btn.addEventListener("click", function () {
            // Remove active class from all buttons
            filterButtons.forEach(b => b.classList.remove("active", "btn-primary"));
            filterButtons.forEach(b => b.classList.add("btn-light"));

            btn.classList.add("active", "btn-primary");
            btn.classList.remove("btn-light");

            const filterVal = btn.getAttribute("data-filter");

            categoriesSections.forEach(section => {
                const secCat = section.getAttribute("data-category");
                if (filterVal === "All" || secCat === filterVal) {
                    section.classList.remove("d-none");
                } else {
                    section.classList.add("d-none");
                }
            });
        });
    });
});
