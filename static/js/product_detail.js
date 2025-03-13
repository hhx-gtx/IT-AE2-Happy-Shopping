function changeQuantity(change) {
    let qtyInput = document.getElementById("quantity");
    let current = parseInt(qtyInput.value);
    if (current + change > 0) {
        qtyInput.value = current + change;
    }
}

function buyNow() {
    let form = document.getElementById("purchase-form");
    form.action = form.getAttribute("data-buy-now-url"); // Set dynamically in HTML
    form.submit();
}