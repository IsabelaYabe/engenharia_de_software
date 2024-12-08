

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
            if(userType == "owner" || userType == "admin") {
                const pages = document.querySelectorAll('.owner');
                pages.forEach(page => {
                    page.style.display = 'block';
                });    }
        })
}



document.addEventListener('DOMContentLoaded', arrangeMenu);