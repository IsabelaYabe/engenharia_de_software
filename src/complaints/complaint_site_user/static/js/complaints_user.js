// Fetch complaints for a vending machine and display them on the page
function fetchComplaints(vendingMachineId) {
    fetch(`/get_complaints/${vendingMachineId}`)
        .then(response => response.json())
        .then(complaints => {
            const complaintsSection = document.getElementById('complaints-section');
            // Clear the complaints section
            complaintsSection.innerHTML = '';
            
            if (complaints.length > 0) {
                complaints.forEach(complaint => {
                    const complaintDiv = document.createElement('div');
                    complaintDiv.innerHTML = `
                        <p><strong>Complaint ID ${complaint.complaint_id}:</strong> ${complaint.text}</p>
                        <p><em>Submitted on ${complaint.timestamp}</em></p>
                    `;
                    complaintsSection.appendChild(complaintDiv);
                });
            } else {
                complaintsSection.innerHTML = '<p>No complaints for this vending machine.</p>';
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Load complaints for the default vending machine when the page loads
document.addEventListener('DOMContentLoaded', function () {
    // Get the default vending machine ID from the hidden input field
    const defaultVendingMachineId = 1;  // Default ID can be set to any machine ID
    fetchComplaints(defaultVendingMachineId);

    // Set the default vending machine ID in the input field
    document.getElementById('vending-machine-id').value = defaultVendingMachineId;
});


