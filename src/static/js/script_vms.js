// Fetch vm information from the server and populate the table
function fetchVmInfo() {
    console.log("Fetching vm info");
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
                row.addEventListener('click', () => handleTableClick(item[0]));
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
    console.log("Fetching vm info done");
    fetch('/get_role')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(userType => {
            console.log(userType);
            if(userType == "user"){
                const comment = document.getElementById('comment');
                comment.style.display = 'block';
                const complaint = document.getElementById('complaint');
                complaint.style.display = 'block';
            }
        })
        

}

function handleTableClick(id) {
    console.log("Table clicked");
    const commentTitle = document.getElementById('comment-title');
    if (commentTitle) {
        commentTitle.textContent = "Tells us what you think 'bout machine " + id;
    }
    const commentButton = document.getElementById('submit-comment');
    if (commentButton) {
        commentButton.setAttribute('data-vm-id', id);
    }

    const complaintTitle = document.getElementById('complaint-title');
    if (complaintTitle) {
        complaintTitle.textContent = "Complain about machine " + id;
    }
    const complaintButton = document.getElementById('submit-complaint');
    if (complaintButton) {
        complaintButton.setAttribute('data-vm-id', id);
    }

    console.log(id);
    fetchComments(id);
    fetchComplaints(id);
}

// Add a new comment for the product
document.getElementById('submit-comment').addEventListener('click', function () {
    console.log("Submit comment clicked");
    const vmId = this.getAttribute('data-vm-id');
    const commentText = document.getElementById('comment-text').value;

    if (!vmId || !commentText) {
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
            id: vmId,
            text: commentText,
            type: 'vending_machine'
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Comment added successfully!');
            fetchComments(vmId);  // Reload comments
        } else {
            alert('Failed to add comment: ' + data.error);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});

// Fetch comments for the product
function fetchComments(vmId) {
    fetch(`/get_comments/${vmId}/vending_machine`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(comments => {
            const commentsList = document.getElementById('comments-list');
            console.log(comments);
            if (commentsList) {
                commentsList.innerHTML = ''; // Clear the comments list
            }
            if(comments.length == 0){
                const commentItem = document.createElement('li');
                commentItem.textContent = "No comments yet!";
                commentsList.appendChild(commentItem);
            }
            else{
            comments["data"].forEach(comment => {
                const commentItem = document.createElement('li');
                console.log(comment);
                commentItem.textContent = comment[1];
                commentsList.appendChild(commentItem);
            });
        }
        })
        .catch(error => {
            console.error('Error fetching comments:', error);
            // Optionally, display an error message to the user
        });
}

// Add a new complaint for the product
document.getElementById('submit-complaint').addEventListener('click', function () {
    console.log("Submit complaint clicked");
    const vmId = this.getAttribute('data-vm-id');
    const complaintText = document.getElementById('complaint-text').value;

    if (!vmId || !complaintText) {
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
            id: this.getAttribute('data-vm-id'),
            text: complaintText,
            type: 'vending_machine'
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Complaint added successfully!');
            fetchComplaints(vmId);  // Reload complaints
        } else {
            alert('Failed to add complaint: ' + data.error);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});

// Fetch complaints for the product
function fetchComplaints(vmId) {
    fetch(`/get_complaints/${vmId}/vending_machine`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(complaints => {
            console.log("mkkmmkmkkmkmm")
            const complaintsList = document.getElementById('complaints-list');
            console.log("nwfenjdfsijdfsij")
            console.log(complaints);
            if (complaintsList) {
                complaintsList.innerHTML = ''; // Clear the complaints list
            }
            if(complaints.length == 0){
                const complaintItem = document.createElement('li');
                complaintItem.textContent = "No complaints yet!";
                complaintsList.appendChild(complaintItem);
            }
            else{
            complaints["data"].forEach(complaint => {
                const complaintItem = document.createElement('li');
                console.log(complaint);
                complaintItem.textContent = complaint[1];
                complaintsList.appendChild(complaintItem);
            });
            
        }
        })
        .catch(error => {
            console.error('Error fetching complaints:', error);
            // Optionally, display an error message to the user
        });
}

// Fetch vm information when the DOM content is fully loaded
document.addEventListener('DOMContentLoaded', fetchVmInfo);

