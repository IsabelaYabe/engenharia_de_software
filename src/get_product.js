/**
 * This script is responsible for loading the details of a specific product
 * from the API based on the product ID passed in the URL. It interacts with
 * the `DatabaseManagerClient` to fetch the product details and dynamically 
 * populate the HTML elements with the corresponding data.
 * 
 * Functions included:
 *  - getProductIdFromUrl: Extracts the product ID from the URL query parameters.
 *  - loadProductDetails: Fetches product details from the API and populates the HTML.
 * 
 * Author: Isabela Yabe
 */
import databaseClient from './databaseClient.js';

/**
 * Retrieves the product ID from the URL's query parameters.
 * This function extracts the `productId` parameter from the URL string.
 * 
 * @returns {string|null} - The product ID if found in the URL, otherwise null.
 */
function getProductIdFromUrl() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('productId');
}

/**
 * Loads product details by fetching the data from the API and populates
 * the relevant HTML elements with the product's name, description, price, and quantity.
 * 
 * @param {string} productId - The ID of the product to be loaded.
 */
async function loadProductDetails(productId) {
    try {
        const itemDetails = ['name', 'description', 'price', 'quantity'];
        await databaseClient.loadItemDetails('product', productId, itemDetails);
    } catch (error) {
        console.error('Error loading product details:', error);
    }
}

/**
 * Extracts the product ID from the URL and attempts to load the product details.
 * If no product ID is found in the URL, a warning message is logged in the console.
 */
const productId = getProductIdFromUrl();

if (productId) {
    loadProductDetails(productId);
} else {
    console.warn('No productId found in URL');
}
