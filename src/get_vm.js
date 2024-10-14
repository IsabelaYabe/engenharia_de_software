/**
 * VendingMachineApp is an object that initializes and manages the vending machine application.
 * It fetches machine details, displays parameters, sets meta parameters, and displays products.
 * It is the bridge between the vending machine data and the webpage.
 */
const VendingMachineApp = {
    /**
     * Initializes the vending machine application.
     * Fetches machine details and displays parameters, meta parameters, and products.
     * Logs an error message if initialization fails.
     */
    init: function() {
        this.getMachineDetails().then(() => {
            this.displayParam();
            this.setMetaParam();
            this.displayProducts();
        }).catch(error => console.error('Initialization failed:', error));
    },

    /**
     * Retrieves the value of a query parameter from the URL.
     * @param {string} param - The name of the query parameter.
     * @returns {string|null} The value of the query parameter, or null if not found.
     */
    getQueryParam: function(param) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(param);
    },

    /**
     * Fetches the details of the vending machine from a JSON file.
     * Logs the machine details if found, otherwise logs an error message.
     * @returns {Promise<void>} A promise that resolves when the machine details are fetched.
     */
    getMachineDetails: function() {
        const machineId = this.getQueryParam('machine_id') || 'vm1';
        if (machineId) {
            return fetch('../data/vending_machines.json') // Retornando a promise aqui
                .then(response => response.json())
                .then(data => {
                    this.data = data;
                    const machineDetails = data[machineId];
                    if (machineDetails) {
                        console.log(machineDetails);
                    } else {
                        console.error('Machine details not found');
                    }
                })
                .catch(error => console.error('Error fetching machine details:', error));
        }
        return Promise.reject('Machine ID not provided');
    },

    /**
     * Displays the parameters of the vending machine on the webpage.
     * Updates the text content of elements with class names 'name', 'location', 'review', 'status', and 'description'.
     */
    displayParam: function() {
        const machineId = this.getQueryParam('machine_id') || 'vm1';
        const machineDetails = this.data[machineId];
        if (machineDetails) {
            document.querySelectorAll('.name').forEach(element => {
                element.innerText = machineDetails.name; // Exibe o nome da máquina
            });
            document.querySelectorAll('.location').forEach(element => {
                element.innerText = machineDetails.location; // Exibe a localização da máquina
            });
            document.querySelectorAll('.review').forEach(element => {
                element.innerText = machineDetails.review; // Exibe a avaliação
            });
            document.querySelectorAll('.status').forEach(element => {
                element.innerText = machineDetails.status; // Exibe o status
            });
            document.querySelectorAll('.description').forEach(element => {
                element.innerText = machineDetails.description; // Exibe a descrição
            });
        }
    },

    /**
     * Sets the meta parameter for the vending machine.
     * Updates the content attribute of the meta tag with name 'keywords'.
     */
    setMetaParam: function() {
        const machineId = this.getQueryParam('machine_id') || '1';
        const machineDetails = this.data[machineId];
        if (machineDetails) {
            document.querySelector('meta[name="keywords"]').setAttribute('content', `vending_machine, ${machineDetails.id}`);
        }
    },

    /**
     * Displays the products of the vending machine on the webpage.
     * Updates the inner HTML of the element with class name 'productsList'.
     * If no products are available, displays a message indicating no products are available.
     */
    displayProducts: function() {
        const machineId = this.getQueryParam('machine_id') || 'vm1';
        const machineDetails = this.data[machineId];
        if (machineDetails) {
            const products = machineDetails.products;
            const productsList = document.querySelector('.productsList');
            if (products && products.length) {
                productsList.innerHTML = products.map(product => {
                    return `<li>${product.name} - R$${product.price}</li>`;
                }).join('');
            } else {
                productsList.innerHTML = '<li>No products available</li>';
            }
        }
    }

};

// Initialize the vending machine application
VendingMachineApp.init();

