/**
 * Constant responsible for managing the complaints screen, including loading and clearing complaints from localStorage.
 */
const complaints_screen_manager = {
    
    /**
     * Function to load complaints from localStorage and display them in the table.
     * Retrieves complaints data and populates the table with user ID, complaint text, and timestamp.
     */
    loadComplaints: function() {
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
    },

    /**
     * Function to clear all complaints from localStorage and refresh the table.
     * Prompts the user for confirmation before clearing the data.
     */
    clearComplaints: function() {
        if (confirm("Are you sure you want to clear all complaints?")) {
            localStorage.removeItem("complaints");
            this.loadComplaints();
        }
    },

    /**
     * Function to load complaints when the page is loaded.
     */
    init: function() {
        window.onload = this.loadComplaints.bind(this);
    }
};

// Initialize complaints screen manager
complaints_screen_manager.init();
