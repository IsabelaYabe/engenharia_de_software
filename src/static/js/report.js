// Fetch stock information from the server and populate the table
function fetchStockInfo() {
    fetch('/get_stock_report')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(stockInfo => {
            const tableBody = document.getElementById('report-table-body');
            tableBody.innerHTML = ''; // Clear the table
            
            stockInfo.forEach(item => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${item.product_name}</td>
                    <td>${item.vending_machine_name}</td>
                    <td>${item.product_quantity}</td>
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
