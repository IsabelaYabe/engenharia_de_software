
    // Fetch stock information from the server and populate the table
    function fetchStockInfo() {
        fetch('/get_stock_info')
            .then(response => response.json())
            .then(stockInfo => {
                const tableBody = document.getElementById('stock-table-body');
                tableBody.innerHTML = ''; // Clear the table
                
                stockInfo.forEach(item => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${item.product_id}</td>
                        <td>${item.product_name}</td>
                        <td>${item.product_price}</td>
                        <td>${item.product_quantity}</td>
                        <td>${item.vending_machine_id}</td>
                        <td>${item.vending_machine_name}</td>
                    `;
                    tableBody.appendChild(row);
                });
            })
            .catch(error => {
                console.error('Error fetching stock info:', error);
            });
    }

    document.addEventListener('DOMContentLoaded', fetchStockInfo);