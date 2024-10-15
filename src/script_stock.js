/**
 * Constant responsible for loading and filtering vending machine stock data using simulated data.
 */
const stockScreen = {
    // Simulated data to represent vending machines and product stock
    vendingMachines: [
        { id: 1, name: "Vending Machine 1", products: [
            { name: "Coca-Cola", stock: 10 },
            { name: "Pepsi", stock: 5 },
            { name: "Mineral Water", stock: 20 }
        ]},
        { id: 2, name: "Vending Machine 2", products: [
            { name: "Chips", stock: 15 },
            { name: "Chocolate", stock: 8 },
            { name: "Orange Juice", stock: 12 }
        ]},
        { id: 3, name: "Vending Machine 3", products: [
            { name: "Biscuit", stock: 25 },
            { name: "Sandwich", stock: 5 },
            { name: "Coffee", stock: 30 }
        ]}
    ],

    /**
     * Function that loads the simulated stock data into the display table.
     * Populates the table with product information and their respective stock levels.
     */
    loadStockTable: function() {
        const tableBody = document.querySelector('#stock-table tbody');
        tableBody.innerHTML = ''; // Clears the table before adding new data

        this.vendingMachines.forEach(machine => {
            machine.products.forEach(product => {
                const row = document.createElement('tr');
                row.classList.add('product-row'); // Adds a class for filtering

                const vmCell = document.createElement('td');
                const productNameCell = document.createElement('td');
                const productStockCell = document.createElement('td');

                vmCell.textContent = machine.name;
                productNameCell.textContent = product.name;
                productStockCell.textContent = product.stock;

                row.appendChild(vmCell);
                row.appendChild(productNameCell);
                row.appendChild(productStockCell);
                tableBody.appendChild(row);
            });
        });
    },

    /**
     * Function responsible for filtering products based on the values entered in the filter fields.
     * Filters by vending machine name and product name.
     */
    filterProducts: function() {
        const vmFilterValue = document.getElementById('vm-filter').value.toLowerCase();
        const productFilterValue = document.getElementById('product-filter').value.toLowerCase();
        const rows = document.querySelectorAll('.product-row');

        rows.forEach(row => {
            const vmName = row.querySelector('td:first-child').textContent.toLowerCase(); // VM name in the first cell
            const productName = row.querySelector('td:nth-child(2)').textContent.toLowerCase(); // Product name in the second cell

            // Checks if the VM name and product name contain the filter values
            if (vmName.includes(vmFilterValue) && productName.includes(productFilterValue)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    },

    /**
     * Function that initializes the stock screen and loads the data when the page loads.
     */
    init: function() {
        window.onload = this.loadStockTable.bind(this);
    }
};

// Initializes the stock screen
stockScreen.init();
