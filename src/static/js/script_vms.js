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
                row.innerHTML = `
                    <td>${item[0]}</td>
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

// Fetch vm information when the DOM content is fully loaded
document.addEventListener('DOMContentLoaded', fetchVmInfo);
