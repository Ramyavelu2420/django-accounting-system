// Bills Client Interactions

document.addEventListener("DOMContentLoaded", function () {
    const tableBody = document.getElementById("bill-items-body");
    const btnAddRow = document.getElementById("btn-add-bill-row");
    const subtotalText = document.getElementById("subtotal-val");
    const discountInput = document.getElementById("discount-input");
    const discountVal = document.getElementById("discount-val");
    const taxInput = document.getElementById("tax-input");
    const taxVal = document.getElementById("tax-val");
    const totalVal = document.getElementById("total-val");
    const itemsDataInput = document.getElementById("items-data-input");

    const hiddenSubtotal = document.getElementById("hidden-subtotal");
    const hiddenDiscount = document.getElementById("hidden-discount");
    const hiddenTax = document.getElementById("hidden-tax");
    const hiddenTotal = document.getElementById("hidden-total");

    // 1. Calculations
    function calculateTotals() {
        let subtotal = 0;
        const rows = tableBody.querySelectorAll("tr");
        const items = [];

        rows.forEach((row) => {
            const selectItem = row.querySelector(".row-item-select");
            const inputName = row.querySelector(".row-item-name");
            const inputDesc = row.querySelector(".row-item-desc");
            const inputQty = row.querySelector(".row-item-qty");
            const inputPrice = row.querySelector(".row-item-price");
            const textAmount = row.querySelector(".row-item-amount");

            const qty = parseFloat(inputQty.value) || 0;
            const price = parseFloat(inputPrice.value) || 0;
            const amount = qty * price;
            textAmount.textContent = "₹" + amount.toFixed(2);
            subtotal += amount;

            items.push({
                item_id: selectItem ? selectItem.value : null,
                name: inputName.value,
                description: inputDesc.value,
                quantity: qty,
                price: price,
                amount: amount
            });
        });

        subtotalText.textContent = "₹" + subtotal.toFixed(2);
        hiddenSubtotal.value = subtotal.toFixed(2);

        const discountPercentage = parseFloat(discountInput.value) || 0;
        const discountAmount = (subtotal * discountPercentage) / 100;
        discountVal.textContent = "₹" + discountAmount.toFixed(2);
        hiddenDiscount.value = discountAmount.toFixed(2);

        const taxPercentage = parseFloat(taxInput.value) || 0;
        const taxAmount = ((subtotal - discountAmount) * taxPercentage) / 100;
        taxVal.textContent = "₹" + taxAmount.toFixed(2);
        hiddenTax.value = taxAmount.toFixed(2);

        const total = subtotal - discountAmount + taxAmount;
        totalVal.textContent = "₹" + total.toFixed(2);
        hiddenTotal.value = total.toFixed(2);

        itemsDataInput.value = JSON.stringify(items);
    }

    // 2. Add Row
    if (btnAddRow && tableBody) {
        btnAddRow.addEventListener("click", function () {
            const newRow = document.createElement("tr");
            newRow.innerHTML = `
                <td>
                    <select class="form-select row-item-select mb-2">
                        <option value="">-- Select Item --</option>
                        ${window.availableItemsList || ''}
                    </select>
                    <input type="text" class="form-control row-item-name" placeholder="Item Name" required>
                </td>
                <td>
                    <textarea class="form-control row-item-desc" rows="1" placeholder="Description"></textarea>
                </td>
                <td>
                    <input type="number" class="form-control row-item-qty" value="1" min="1" step="1" style="width: 80px;">
                </td>
                <td>
                    <input type="number" class="form-control row-item-price" value="0.00" min="0" step="0.01" style="width: 120px;">
                </td>
                <td class="text-end fw-semibold row-item-amount">₹0.00</td>
                <td class="text-center">
                    <button type="button" class="btn btn-outline-danger btn-sm btn-delete-row"><i class="bi bi-trash"></i></button>
                </td>
            `;
            tableBody.appendChild(newRow);
            bindRowListeners(newRow);
            calculateTotals();
        });
    }

    function bindRowListeners(row) {
        const select = row.querySelector(".row-item-select");
        const nameInput = row.querySelector(".row-item-name");
        const descInput = row.querySelector(".row-item-desc");
        const qtyInput = row.querySelector(".row-item-qty");
        const priceInput = row.querySelector(".row-item-price");
        const btnDelete = row.querySelector(".btn-delete-row");

        if (select) {
            select.addEventListener("change", function () {
                const selectedOption = select.options[select.selectedIndex];
                if (selectedOption && select.value !== "") {
                    nameInput.value = selectedOption.getAttribute("data-name") || "";
                    descInput.value = selectedOption.getAttribute("data-desc") || "";
                    priceInput.value = parseFloat(selectedOption.getAttribute("data-price")) || 0;
                } else {
                    nameInput.value = "";
                    descInput.value = "";
                    priceInput.value = "0.00";
                }
                calculateTotals();
            });
        }

        qtyInput.addEventListener("input", calculateTotals);
        priceInput.addEventListener("input", calculateTotals);

        btnDelete.addEventListener("click", function () {
            row.remove();
            calculateTotals();
        });
    }

    if (tableBody) {
        tableBody.querySelectorAll("tr").forEach(row => {
            bindRowListeners(row);
        });
        calculateTotals();
    }

    if (discountInput) discountInput.addEventListener("input", calculateTotals);
    if (taxInput) taxInput.addEventListener("input", calculateTotals);

    // 3. Vendor popup modal trigger
    const selectVendorPlaceholder = document.getElementById("vendor-placeholder-box");
    const vendorFormSection = document.getElementById("vendor-form-section");
    const vendorModalElement = document.getElementById("addVendorModal");
    let vendorModal = null;
    if (vendorModalElement) {
        vendorModal = new bootstrap.Modal(vendorModalElement);
    }

    if (selectVendorPlaceholder && vendorFormSection && vendorModal) {
        selectVendorPlaceholder.addEventListener("click", () => {
            vendorModal.show();
        });
    }

    const vendorForm = document.getElementById("ajax-vendor-form");
    const vendorSelect = document.getElementById("id_vendor");
    if (vendorForm && vendorSelect && vendorModal) {
        vendorForm.addEventListener("submit", function (e) {
            e.preventDefault();
            // Simulating inline saving for demo purposes, adding to selection
            const vendorName = document.getElementById("id_vendor_name").value;
            if (vendorName) {
                const newOpt = new Option(vendorName, "1", true, true);
                vendorSelect.add(newOpt);
                vendorSelect.value = "1";
                vendorForm.reset();
                vendorModal.hide();
                
                selectVendorPlaceholder.classList.add("d-none");
                vendorFormSection.classList.remove("d-none");
            }
        });
    }

    // 4. Drag and Drop for Excel Imports
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
