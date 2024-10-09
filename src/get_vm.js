const VendingMachineApp = {
    init: function() {
        this.getMachineDetails().then(() => {
            this.displayParam();
            this.setMetaParam();
            this.displayProducts();
        }).catch(error => console.error('Initialization failed:', error));
    },

    getQueryParam: function(param) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(param);
    },

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

    setMetaParam: function() {
        const machineId = this.getQueryParam('machine_id') || '1';
        const machineDetails = this.data[machineId];
        if (machineDetails) {
            document.querySelector('meta[name="keywords"]').setAttribute('content', `vending_machine, ${machineDetails.id}`);
        }
    },

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

VendingMachineApp.init();
