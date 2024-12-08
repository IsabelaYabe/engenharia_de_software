

function arrangeMenu() {
    fetch('/get_role')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(userType => {
            console.log(userType);
            if(userType == "owner"){
                const comment = document.getElementById('owner');
                comment.style.display = 'block';
            }
        })
}



document.addEventListener('DOMContentLoaded', arrangeMenu);