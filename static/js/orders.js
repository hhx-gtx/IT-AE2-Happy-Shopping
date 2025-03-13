let deleteMode = false;

function toggleDeleteMode() {
    deleteMode = !deleteMode;
    let checkboxes = document.querySelectorAll(".orderCheckbox");
    let deleteBtn = document.getElementById("deleteSelected");
    let selectAll = document.getElementById("selectAll");
    let tableHead = document.getElementById("orderTableHead");

    if (deleteMode) {
        checkboxes.forEach(cb => cb.style.display = "inline");
        deleteBtn.style.display = "block";
        selectAll.style.display = "inline";
        tableHead.style.display = "table-header-group";
    } else {
        checkboxes.forEach(cb => cb.style.display = "none");
        deleteBtn.style.display = "none";
        selectAll.style.display = "none";
        tableHead.style.display = "none";
    }
}

function toggleSelectAll() {
    let checkboxes = document.querySelectorAll(".orderCheckbox");
    let selectAll = document.getElementById("selectAll");
    checkboxes.forEach(cb => cb.checked = selectAll.checked);
}
