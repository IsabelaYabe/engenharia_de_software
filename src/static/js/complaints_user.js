document.getElementById('submit-complaint').addEventListener('click', function () {
    const vendingMachineId = document.getElementById('vending-machine-id').value || null;
    const complaintText = document.getElementById('complaint-text').value;

    if (!complaintText) {
        alert("Please enter the complaint text.");
        return;
    }

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
