from hashlib import sha256

class AuthManager:
    def __init__(self, manager_profile):
        self.manager_profile = manager_profile

    def hash_password(self, password):
        return sha256(password.encode()).hexdigest()
    
    def login(self, username, password):
        hashed_password = self.hash_password(password)
        query = f"SELECT * FROM {self.manager_profile} WHERE username = {username} AND password = {hashed_password};"

        try:
            user = self.manager_profile._execute_sql(query, fetch_one=True)
            if user:
                return user
            else:
                return None
        except Exception as e:
            return None