// Function to create a widget for a product
function createProductWidget(product) {
    const widget = document.createElement('div');
    widget.className = 'product-widget';
    console.log(product);
    widget.innerHTML = `
        <h3>${product[1]}</h3>
        <p>${product[2]}</p>
        <p>Price: ${product[3]}</p>
        <p>Quantity: ${product[4]}</p>
        <button class="btn btn-primary">Add to Cart</button>
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
function fetchVmInfo(item) {
    fetch(`/get_vm_products/${item.id}`)
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
document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname; // Exemplo: "/vm_profile/1"
    const segments = path.split('/'); // Divide a URL em partes, como ["", "vm_profile", "1"]
    const id = segments[segments.length - 1]; // Pega o último segmento, que é o "1"
    console.log(id);

    // Você pode usar o ID para buscar informações
    const item = { "id": id };
    fetchVmInfo(item);
});