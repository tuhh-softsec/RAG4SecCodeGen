import bcrypt
import sqlite3
from getpass import getpass

# Function to hash a password
def hash_password(password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

# Function to insert a new user into the database
def insert_user(username, password):
    # Hash the password
    hashed_password = hash_password(password)
    
    # Encrypt the username here if necessary (not shown for simplicity)
    # encrypted_username = encrypt(username)
    
    # Insert the username and hashed password into the database
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()

# Function to authenticate a user
def authenticate_user(username, password):
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        user_record = cursor.fetchone()
        
        if user_record:
            stored_hash = user_record[0]
            # Compare the hash of the incoming password to the saved hash
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                return True
            else:
                return False
        else:
            return False

# Main function to handle user registration and login
def main():
    action = input("Do you want to register or login? (register/login): ").strip().lower()
    
    if action == "register":
        username = input("Enter a new username: ")
        password = getpass("Enter a new password: ")
        insert_user(username, password)
        print("Registration successful.")
    elif action == "login":
        username = input("Enter your username: ")
        password = getpass("Enter your password: ")
        if authenticate_user(username, password):
            print("Login successful.")
        else:
            print("Login failed. Incorrect username or password.")
    else:
        print("Invalid action.")

if __name__ == "__main__":
    main()

