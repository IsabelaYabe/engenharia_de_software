document.getElementById('submit-complaint').addEventListener('click', function () {
    const vendingMachineId = document.getElementById('vending-machine-id').value;
    const userId = document.getElementById('user-id').value;  
    const complaintText = document.getElementById('complaint-text').value;

    if (!vendingMachineId || !userId || !complaintText) {
        alert("Please fill in all fields.");
        return;
    }

    fetch('/add_complaint', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            vending_machine_id: vendingMachineId,
            user_id: userId,  
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
