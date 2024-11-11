import DatabaseManagerClient from './databaseClient.js';

const client = new DatabaseManagerClient('http://localhost:5000');

async function loadProduct(productId) {
    const productDetails = await client.getRecordById('product', productId);

    if (productDetails) {
        document.querySelector('.name').textContent = productDetails.name;
        document.querySelector('.description').textContent = productDetails.description;
        document.querySelector('.price').textContent = `$${productDetails.price}`;
        document.querySelector('.quantity').textContent = productDetails.quantity;
    } else {
        document.getElementById("error-message").style.display = "block";
    }
}

const productId = new URLSearchParams(window.location.search).get('productId');
if (productId) {
    loadProduct(productId);
} else {
    console.warn('Nenhum produto encontrado');
}
