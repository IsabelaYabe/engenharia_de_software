// Load complaints from localStorage and display in the table
function loadComplaints() {
    const complaints = JSON.parse(localStorage.getItem("complaints")) || [];
    const tableBody = document.getElementById("complaintsTableBody");

    // Clear any previous rows
    tableBody.innerHTML = "";

    complaints.forEach((complaint) => {
        const row = document.createElement("tr");

        const userIdCell = document.createElement("td");
        userIdCell.textContent = complaint.user_id;
        row.appendChild(userIdCell);

        const textCell = document.createElement("td");
        textCell.textContent = complaint.text;
        row.appendChild(textCell);

        const timestampCell = document.createElement("td");
        timestampCell.textContent = complaint.timestamp;
        row.appendChild(timestampCell);

        tableBody.appendChild(row);
    });
}

// Clear all complaints from localStorage and refresh the table
function clearComplaints() {
    if (confirm("Are you sure you want to clear all complaints?")) {
        localStorage.removeItem("complaints");
        loadComplaints();
    }
}

// Load complaints on page load
window.onload = loadComplaints;
