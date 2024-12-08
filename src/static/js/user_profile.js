// Function to create a widget for a product
function createBio(bio) {
    const widget = document.createElement('div');
    widget.className = 'bio-widget';
    console.log(bio);
    widget.innerHTML = `
        <h3>${bio[1]}</h3>
        <p>${bio[2]}</p>
        <p>Price: ${bio[3]}</p>
        <p>Quantity: ${bio[4]}</p>
        <button class="btn btn-primary">Add to Cart</button>
    `;
    return widget;
}

// Modify fetchVmInfo to use displayProductWidgets
function fetchUserInfo(item) {
    fetch(`/get_user_info`)
        .then(response => {
            console.log(response);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(bio => {
            console.log(bio);
            createBio(bio);
        })
        .catch(error => {
            console.error(`Error fetching products for VM ${item.id}:`, error);
            const container = document.getElementById('product-widgets-container');
            container.innerHTML = 'Error fetching products';
        });
}

// Fetch vm information when the DOM content is fully loaded
document.addEventListener('DOMContentLoaded', fetchUserInfo);