// Fetch complaints and display them on the page
function fetchComplaints() {
    fetch('/get_complaints')
        .then(response => response.json())
        .then(complaints => {
            console.log(complaints);
            const complaintsSection = document.getElementById('complaints-section');
            // Clear the complaints section
            complaintsSection.innerHTML = '';
            
            if (complaints.length > 0) {
                complaints.forEach(complaint => {
                    console.log(complaint);
                    const complaintRow = document.createElement('tr');
                    complaintRow.innerHTML = `
                        <td>${complaint.complaint_id}</td>
                        <td>${complaint.timestamp}</td>
                        <td>${complaint.vending_machine_id}</td>
                        <td>${complaint.vm_name}</td>
                        <td>${complaint.text}</td>
                        <td>${complaint.user_id}</td> <!-- Adicionando a coluna para UserID -->
                    `;
                    complaintsSection.appendChild(complaintRow);
                });
            } else {
                complaintsSection.innerHTML = '<tr><td colspan="6">No complaints available.</td></tr>'; // Ajustado para 6 colunas
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
