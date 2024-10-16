/**
 * Constant responsible for handling user complaint submissions, validation, and storing in localStorage.
 */
const complaints_screen_user = {
    
    // Define banned words for complaints
    bannedWords: ["curseword1", "curseword2", "curseword3"],

    /**
     * Function to submit a complaint. Validates the complaint text, checks for banned words,
     * stores the complaint in localStorage, and displays appropriate messages.
     */
    submitComplaint: function() {
        // Get input values
        const userId = document.getElementById("user_id").value;
        const complaintText = document.getElementById("complaint_text").value.trim();

        // Reference to the message element
        const messageElement = document.getElementById("message");

        // Clear previous message
        messageElement.classList.add("hidden");
        messageElement.textContent = "";

        // Validate complaint text
        if (complaintText === "") {
            this.showMessage("Complaint has no text", "error");
            return;
        }

        if (this.containsBannedWords(complaintText)) {
            this.showMessage("Complaint contains inappropriate language", "error");
            return;
        }

        // Simulate successful submission
        const timestamp = new Date().toLocaleString();

        // Create complaint object
        const complaint = {
            user_id: userId,
            text: complaintText,
            timestamp: timestamp
        };

        // Store complaint in localStorage
        this.saveComplaint(complaint);

        // Show success message
        const successMessage = `Complaint successfully submitted by ${userId} on ${timestamp}.`;
        this.showMessage(successMessage, "success");

        // Clear the form fields after submission
        document.getElementById("user_id").value = "";
        document.getElementById("complaint_text").value = "";
    },

    /**
     * Helper function to check if the complaint text contains any banned words.
     * @param {string} text - The complaint text to be validated.
     * @returns {boolean} - Returns true if the text contains banned words, otherwise false.
     */
    containsBannedWords: function(text) {
        return this.bannedWords.some(word => text.toLowerCase().includes(word));
    },

    /**
     * Helper function to display a message on the screen.
     * @param {string} message - The message to display.
     * @param {string} type - The type of the message ("error" or "success").
     */
    showMessage: function(message, type) {
        const messageElement = document.getElementById("message");
        messageElement.textContent = message;
        messageElement.classList.remove("hidden");
        messageElement.className = type === "error" ? "error" : "success";
    },

    /**
     * Function to save the complaint to localStorage.
     * @param {Object} complaint - The complaint object containing user_id, text, and timestamp.
     */
    saveComplaint: function(complaint) {
        let complaints = JSON.parse(localStorage.getItem("complaints")) || [];
        complaints.push(complaint);
        localStorage.setItem("complaints", JSON.stringify(complaints));
    }
};
