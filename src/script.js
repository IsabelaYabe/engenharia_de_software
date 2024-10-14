// Define banned words for complaints
const bannedWords = ["curseword1", "curseword2", "curseword3"];

// Function to submit a complaint
function submitComplaint() {
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
        showMessage("Complaint has no text", "error");
        return;
    }

    if (containsBannedWords(complaintText)) {
        showMessage("Complaint contains inappropriate language", "error");
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
    saveComplaint(complaint);

    // Show success message
    const successMessage = `Complaint successfully submitted by ${userId} on ${timestamp}.`;
    showMessage(successMessage, "success");

    // Clear the form fields after submission
    document.getElementById("user_id").value = "";
    document.getElementById("complaint_text").value = "";
}

// Helper function to check if the text contains any banned words
function containsBannedWords(text) {
    return bannedWords.some(word => text.toLowerCase().includes(word));
}

// Helper function to display a message
function showMessage(message, type) {
    const messageElement = document.getElementById("message");
    messageElement.textContent = message;
    messageElement.classList.remove("hidden");
    messageElement.className = type === "error" ? "error" : "success";
}

// Save complaint to localStorage
function saveComplaint(complaint) {
    let complaints = JSON.parse(localStorage.getItem("complaints")) || [];
    complaints.push(complaint);
    localStorage.setItem("complaints", JSON.stringify(complaints));
}
