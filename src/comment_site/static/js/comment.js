// Get comments for a product and display them on the page
function fetchComments(productId) {
    fetch(`/get_comments/${productId}`)
        .then(response => response.json())
        .then(comments => {
            const commentsSection = document.getElementById('comments-section');
            // Clear the comments section
            commentsSection.innerHTML = '';
            
            if (comments.length > 0) {
                comments.forEach(comment => {
                    const commentDiv = document.createElement('div');
                    commentDiv.innerHTML = `
                        <p><strong>User ${comment.user_id}:</strong> ${comment.text}</p>
                        <p><em>Posted on ${comment.timestamp}</em></p>
                    `;
                    commentsSection.appendChild(commentDiv);
                });
            } else {
                commentsSection.innerHTML = '<p>No comments for this product.</p>';
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Load comments for the default product when the page loads
document.addEventListener('DOMContentLoaded', function () {
    // Get the default product ID from the hidden input field
    const defaultProductId = 1
    fetchComments(defaultProductId);

    // Set the default product ID in the input field
    document.getElementById('product-id').value = defaultProductId;
});

// Add a new comment for the product
document.getElementById('submit-comment').addEventListener('click', function () {
    const productId = document.getElementById('product-id').value;
    const userId = document.getElementById('user-id').value;
    const commentText = document.getElementById('comment-text').value;

    if (!productId || !userId || !commentText) {
        alert("Please fill in all fields.");
        return;
    }

    // Send a POST request to the server with the new comment data
    fetch('/add_comment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            product_id: productId,
            user_id: userId,
            text: commentText
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Comment added successfully!');
            fetchComments(productId);  // Reload comments
        } else {
            alert('Failed to add comment.');
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});
