// Fetch all complaints from the database and display them on the page
function fetchAllComplaints() {
    fetch('/get_all_complaints')
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
                complaintsSection.innerHTML = '<p>No complaints found.</p>';
            }
        })
        .catch(error => {
            console.error('Error fetching complaints:', error);
        });
}

// Load all complaints when the page loads
document.addEventListener('DOMContentLoaded', function () {
    fetchAllComplaints();
});
