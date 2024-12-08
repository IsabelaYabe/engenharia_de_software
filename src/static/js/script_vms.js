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
                `;
                tableBody.appendChild(row);

                /*
                fetch(`/get_vm_products/${item.id}`)
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
                */
            });
        })
        .catch(error => {
            console.error('Error fetching vm info:', error);
            // Optionally, display an error message to the user
        });
}

// Fetch vm information when the DOM content is fully loaded
document.addEventListener('DOMContentLoaded', fetchVmInfo);
