// Fetch stock information from the server and populate the table
function fetchStockInfo() {
    fetch('/get_stock_info')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(stockInfo => {
            const tableBody = document.getElementById('stock-table-body');
            tableBody.innerHTML = ''; // Clear the table
            console.log(stockInfo);
            stockInfo["data"].forEach(item => {
                const row = document.createElement('tr');
                console.log(item);
                row.innerHTML = `
                    <td>${item.vm_id}</td>
                    <td>${item.vm_name}</td>
                    <td>${item.product_id}</td>
                    <td>${item.product_name}</td>
                    <td>${item.quantity}</td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error fetching stock info:', error);
            // Optionally, display an error message to the user
        });
}

// Fetch stock information when the DOM content is fully loaded
document.addEventListener('DOMContentLoaded', fetchStockInfo);
