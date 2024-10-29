import DatabaseManagerClient from './databaseClient.js';

// Inicializar o client com a URL base da API
const client = new DatabaseManagerClient('http://localhost:5000');

// Função para carregar o produto na página
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

// Pegar o ID do produto da URL e carregar os detalhes
const productId = new URLSearchParams(window.location.search).get('productId');
if (productId) {
    loadProduct(productId);
} else {
    console.warn('Nenhum produto encontrado');
}
