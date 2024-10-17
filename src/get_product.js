import databaseClient from './databaseClient.js';

function getProductIdFromUrl() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('productId');
}

async function loadProductDetails(productId) {
    try {
        const itemDetails = ['name', 'description', 'price', 'quantity'];
        await databaseClient.loadItemDetails('product', productId, itemDetails);
    } catch (error) {
        console.error('Error loading product details:', error);
    }
}

const productId = getProductIdFromUrl();

if (productId) {
    loadProductDetails(productId);
} else {
    console.warn('No productId found in URL');
}
