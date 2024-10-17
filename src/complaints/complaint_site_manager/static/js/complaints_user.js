


// Add a new complaint for the vending machine
document.getElementById('submit-complaint').addEventListener('click', function () {
    const vendingMachineId = document.getElementById('vending-machine-id').value;
    const complaintText = document.getElementById('complaint-text').value;

    if (!vendingMachineId || !complaintText) {
        alert("Please fill in all fields.");
        return;
    }

    // Send a POST request to the server with the new complaint data
    fetch('/add_complaint', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            vending_machine_id: vendingMachineId,
            text: complaintText
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Complaint added successfully!');
        } else {
            alert('Failed to add complaint: ' + data.error);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});
