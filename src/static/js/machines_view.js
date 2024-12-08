function withdraw(vm_id) {
    const quantitySelector = document.querySelector('#quantity-selector-' + vm_id);
    const amount = quantitySelector.value;
    console.log('Withdraw money from vending machine:', vm_id);
    fetch('/withdraw_vm', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            amount: amount,
            vending_machine_id: vm_id
        })
    })
        .then(response => {
            console.log(response);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            alert('Product purchased successfully!');
        })
        .catch(error => {
            console.error('Error buying product:', error);
            alert('Error buying product');
        });
    }

// Function to create a widget for a product
function createProductWidget(product) {
    const widget = document.createElement('div');
    widget.className = 'product-widget';
    console.log(product);
    widget.innerHTML = `
        <h3>${product[1]}</h3>
        <p>${product[2]}</p>
        <p>Status: ${product[3]}</p>
        <p>Budget: ${product[4]}</p>
        <input type="number" id="quantity-selector-${product[0]}" class="quantity-selector" min="0" max=${product[4]} value="1">
        <button onclick="withdraw(${product[0]})" class="btn btn-primary">Buy right now!</button>
    `;
    return widget;
}

// Function to display products in widgets
function displayProductWidgets(products) {
    console.log(products);
    const container = document.getElementById('product-widgets');
    container.innerHTML = ''; // Clear any existing widgets
    products.forEach(product => {
        console.log(product);
        const widget = createProductWidget(product);
        container.appendChild(widget);
    });
}

// Modify fetchVmInfo to use displayProductWidgets
function fetchVmInfo() {
    fetch(`/get_vm_particular`)
        .then(response => {
            console.log(response);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(products => {
            items = products["data"];
            displayProductWidgets(items);
        })
        .catch(error => {
            console.error(`Error fetching products for VM ${item.id}:`, error);
            const container = document.getElementById('product-widgets-container');
            container.innerHTML = 'Error fetching products';
        });
}

// Fetch vm information when the DOM content is fully loaded
document.addEventListener('DOMContentLoaded', fetchVmInfo());
