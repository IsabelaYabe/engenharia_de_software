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
            const tableBody = document.getElementById('vm-table-body');
            tableBody.innerHTML = ''; // Clear the table
            
            vmInfo.forEach(item => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${item.VMID}</td>
                    <td>${item.Name}</td>
                    <td>${item.Location}</td>
                    <td>${item.OwnerID}</td>
                    <td>${item.Status}</td>
                `;
                tableBody.appendChild(row);

                fetch(`/get_vm_products/${item.VMID}`)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    })
                    .then(products => {
                        const productsCell = document.createElement('td');
                        productsCell.innerHTML = products.map(product => product.Name).join(', ');
                        row.appendChild(productsCell);
                    })
                    .catch(error => {
                        console.error(`Error fetching products for VM ${item.VMID}:`, error);
                        const productsCell = document.createElement('td');
                        productsCell.innerHTML = 'Error fetching products';
                        row.appendChild(productsCell);
                    });
            });
        })
        .catch(error => {
            console.error('Error fetching vm info:', error);
            // Optionally, display an error message to the user
        });
}

// Fetch vm information when the DOM content is fully loaded
document.addEventListener('DOMContentLoaded', fetchVmInfo);
