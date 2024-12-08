// Function to create a widget for a product
function createBio(bio) {
    const widget = document.createElement('div');
    widget.className = 'bio-widget';
    console.log(bio);
    widget.innerHTML = `
        <h3 style="padding-left: 50px;">${bio["username"]}</h3>
        <p style="padding-left: 50px;">${bio["email"]}</p>
        <p style="padding-left: 50px;">Name: ${bio["first_name"]} ${bio["last_name"]}</p>
        <p style="padding-left: 50px;">Birthday: ${bio["birthdate"]}</p>
        <p style="padding-left: 50px;">Phone: ${bio["phone_number"]}</p>
        <p style="padding-left: 50px;">Address: ${bio["address"]}</p>
        <p style="padding-left: 50px;">Budget: ${bio["budget"]}</p>
        <p style="padding-left: 50px;">Role: ${bio["user_type"]}</p>
    `;
    document.body.appendChild(widget);
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