// Fetch complaints and display them on the page
function fetchComplaints() {
    fetch('/get_complaints')
        .then(response => response.json())
        .then(complaints => {
            const complaintsSection = document.getElementById('complaints-section');
            // Clear the complaints section
            complaintsSection.innerHTML = '';
            
            if (complaints.length > 0) {
                complaints.forEach(complaint => {
                    console.log(complaint);
                    const complaintRow = document.createElement('tr');
                    complaintRow.innerHTML = `
                        <td>${complaint.complaint_id}</td>
                        <td>${complaint.user_id}</td>
                        <td>${complaint.user_name}</td>
                        <td>${complaint.text}</td>
                        <td>${complaint.timestamp}</td>
                    `;
                    complaintsSection.appendChild(complaintRow);
                });
            } else {
                complaintsSection.innerHTML = '<tr><td colspan="5">No complaints for this vending machine.</td></tr>';
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Load complaints when the page loads
document.addEventListener('DOMContentLoaded', function () {
    fetchComplaints();
});