// Defining banned words (cursewords)
const bannedWords = ["curseword1", "curseword2", "curseword3"]; // Example of banned words

/**
 * Object to manage comment-related functionality.
 */
const comment = {
    /**
     * Submits a comment after performing validation.
     * Checks if the comment text is empty, contains banned words, and validates the username.
     * Stores the comment and displays it on the screen.
     */
    submitComment() {
        // Retrieve input values
        const user = document.getElementById("user").value.trim();
        const commentText = document.getElementById("comment_text").value.trim();
        const messageElement = document.getElementById("message");

        // Clear previous message
        messageElement.classList.add("hidden");
        messageElement.textContent = "";

        // Validate empty comment text
        if (commentText === "") {
            screen_comment.showMessage("Comment has no text", "error");
            return;
        }

        // Check if the comment contains banned words
        if (this.containsBannedWords(commentText)) {
            screen_comment.showMessage("Comment contains inappropriate language", "error");
            return;
        }

        // Validate username
        if (user === "") {
            screen_comment.showMessage("User name is required", "error");
            return;
        }

        // Create a new comment object
        const timestamp = new Date().toLocaleString();
        const newComment = {
            user: user,
            text: commentText,
            timestamp: timestamp
        };

        // Store the comment in localStorage
        this.saveComment(newComment);

        // Display success message
        screen_comment.showMessage(`Comment successfully submitted by ${user} on ${timestamp}.`, "success");

        // Clear form fields after submission
        document.getElementById("user").value = "";
        document.getElementById("comment_text").value = "";

        // Display the new comment immediately
        screen_comment.addCommentToDisplay(newComment);
    },

    /**
     * Checks if the text contains any banned words.
     * @param {string} text - The comment text to check.
     * @returns {boolean} - Returns true if banned words are found, otherwise false.
     */
    containsBannedWords(text) {
        return bannedWords.some(word => text.toLowerCase().includes(word));
    },

    /**
     * Saves the comment to localStorage.
     * @param {Object} newComment - The comment object containing user, text, and timestamp.
     */
    saveComment(newComment) {
        let comments = JSON.parse(localStorage.getItem("comments")) || [];
        comments.push(newComment);
        localStorage.setItem("comments", JSON.stringify(comments));
    },

    /**
     * Loads comments from localStorage and displays them on the screen.
     */
    loadComments() {
        const comments = JSON.parse(localStorage.getItem("comments")) || [];
        comments.forEach(comment => screen_comment.addCommentToDisplay(comment));
    }
};

/**
 * Object to manage screen-related functionality for comments.
 */
const screen_comment = {
    /**
     * Displays a message (error or success) on the screen.
     * @param {string} message - The message to display.
     * @param {string} type - The type of message ('error' or 'success').
     */
    showMessage(message, type) {
        const messageElement = document.getElementById("message");
        messageElement.textContent = message;
        messageElement.classList.remove("hidden");
        messageElement.className = type === "error" ? "error" : "success";
    },

    /**
     * Adds a single comment to the display section.
     * @param {Object} newComment - The comment object to display.
     */
    addCommentToDisplay(newComment) {
        const commentsContainer = document.getElementById("comments");

        const commentElement = document.createElement("div");
        commentElement.classList.add("comment");

        const userElement = document.createElement("p");
        userElement.textContent = `${newComment.user}:`;
        commentElement.appendChild(userElement);

        const textElement = document.createElement("p");
        textElement.textContent = newComment.text;
        commentElement.appendChild(textElement);

        const timestampElement = document.createElement("p");
        timestampElement.classList.add("timestamp");
        timestampElement.textContent = `Posted on: ${newComment.timestamp}`;
        commentElement.appendChild(timestampElement);

        commentsContainer.appendChild(commentElement);
    }
};

// Load comments when the page is loaded
window.onload = function() {
    comment.loadComments();
};
