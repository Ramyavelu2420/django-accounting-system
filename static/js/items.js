// Items Module interactions

document.addEventListener("DOMContentLoaded", function () {
    // 1. Product/Service Toggle Buttons (New Item Form)
    const btnProduct = document.getElementById("btn-type-product");
    const btnService = document.getElementById("btn-type-service");
    const typeInput = document.getElementById("id_type");

    if (btnProduct && btnService && typeInput) {
        btnProduct.addEventListener("click", function () {
            btnProduct.classList.add("active");
            btnService.classList.remove("active");
            typeInput.value = "product";
        });

        btnService.addEventListener("click", function () {
            btnService.classList.add("active");
            btnProduct.classList.remove("active");
            typeInput.value = "service";
        });
    }

    // 2. Billing: Sale & Purchase Information Checkbox toggles
    const chkSale = document.getElementById("id_sale_enabled");
    const chkPurchase = document.getElementById("id_purchase_enabled");

    const salePrice = document.getElementById("id_sale_price");
    const incomeAccount = document.getElementById("id_income_account");
    const purchasePrice = document.getElementById("id_purchase_price");
    const expenseAccount = document.getElementById("id_expense_account");

    if (chkSale && salePrice && incomeAccount) {
        function toggleSaleInputs() {
            const isChecked = chkSale.checked;
            salePrice.disabled = !isChecked;
            incomeAccount.disabled = !isChecked;
            if (isChecked) {
                salePrice.setAttribute("required", "required");
            } else {
                salePrice.removeAttribute("required");
            }
        }
        chkSale.addEventListener("change", toggleSaleInputs);
        toggleSaleInputs(); // Run once at start
    }

    if (chkPurchase && purchasePrice && expenseAccount) {
        function togglePurchaseInputs() {
            const isChecked = chkPurchase.checked;
            purchasePrice.disabled = !isChecked;
            expenseAccount.disabled = !isChecked;
            if (isChecked) {
                purchasePrice.setAttribute("required", "required");
            } else {
                purchasePrice.removeAttribute("required");
            }
        }
        chkPurchase.addEventListener("change", togglePurchaseInputs);
        togglePurchaseInputs(); // Run once at start
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
