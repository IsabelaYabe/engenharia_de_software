// Fetch vm information from the server and populate the table
function fetchVmInfo() {
    fetch('/get_vm_info')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(vmInfo => {
            console.log(vmInfo);
            head = vmInfo["header"];
            body = vmInfo["data"];
            const tableBody = document.getElementById('vm-table-body');
            tableBody.innerHTML = ''; // Clear the table

            console.log(vmInfo);
            
            body.forEach(item => {
                const row = document.createElement('tr');
                row.style.cursor = 'pointer';
                row.addEventListener('click', handleTableClick);
                row.innerHTML = `
                    <td>${item[1]}</td>
                    <td>${item[2]}</td>
                    <td>${item[4]}</td>
                    <td>${item[3]}</td>
                    <td><button class="btn btn-primary" onclick="window.location.href='/vm_profile/${item[0]}'">View</button></td>
                `;
                tableBody.appendChild(row);

            
                
            });
        })
        .catch(error => {
            console.error('Error fetching vm info:', error);
            // Optionally, display an error message to the user
        });
}

function handleTableClick() {
    console.log("Table clicked");
}

// Add a new comment for the product
document.getElementById('submit-comment').addEventListener('click', function () {
    const productId = document.getElementById('product-id').value;
    const userId = document.getElementById('user-id').value;
    const commentText = document.getElementById('comment-text').value;

    if (!productId || !userId || !commentText) {
        alert("Please fill in all fields.");
        return;
    }

    // Send a POST request to the server with the new comment data
    fetch('/add_comment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            product_id: productId,
            user_id: userId,
            text: commentText
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Comment added successfully!');
            fetchComments(productId);  // Reload comments
        } else {
            alert('Failed to add comment: ' + data.error);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});

// Fetch vm information when the DOM content is fully loaded
document.addEventListener('DOMContentLoaded', fetchVmInfo);

