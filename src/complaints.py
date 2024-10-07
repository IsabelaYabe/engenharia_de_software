import datetime

class Complaint:
    """
    Complaint class
    
    Attributes:
    - banned_words: list
        List of words that are not allowed in complaints
    - user_id: str
        The id of the user submitting the complaint
    - timestamp: datetime
        The date and time when the complaint was submitted
    - vending_machine_id: str, optional
        The ID of the vending machine (if the complaint is about a vending machine)
    - text: str
        The text of the complaint submitted by the user

    Methods:
    - __init__: initialize a new Complaint object with user, text, and optional vending machine ID
    - submit_complaint: submit a complaint after validating the text
    """
    
    banned_words = ["curseword1", "curseword2", "curseword3"]  # Example of prohibited words

    def __init__(self, user_id, text, vending_machine_id=None):
        """
        Initialize a new Complaint object

        Attributes:
        - user: str
            The name or identifier of the user submitting the complaint
        - text: str
            The text of the complaint submitted by the user
        - vending_machine_id: str, optional
            The ID of the vending machine (if applicable)
        """
        self.user_id = user_id
        self.timestamp = datetime.now()
        self.vending_machine_id = vending_machine_id
        self.text = text

    @staticmethod
    def submit_complaint(text, user_id, vending_machine_id=None):
        """
        Submit a complaint after validating the text

        Parameters:
        - text: str
            The text of the complaint
        - user: str
            The name or identifier of the user submitting the complaint
        - vending_machine_id: str, optional
            The ID of the vending machine (if applicable)

        Returns:
        - str: Message indicating the result of the complaint submission
        """
        # Check if the complaint text is empty
        if not text.strip():
            return "Complaint has no text"
        
        # Check if the text contains banned words
        if any(banned_word in text.lower() for banned_word in Complaint.banned_words):
            return "Complaint contains inappropriate language"

        # Create a new complaint instance
        complaint = Complaint(user=user_id, text=text, vending_machine_id=vending_machine_id)

        # Simulate successful submission
        return f"Complaint successfully submitted by {complaint.user} on {complaint.timestamp}. " \
               f"{'Regarding vending machine: ' + vending_machine_id if vending_machine_id else ''}"
