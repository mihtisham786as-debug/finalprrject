import bcrypt
import os

# The file where we will store the users' data (username, hashed password, and role)
USERS_FILE = "users.txt"  # Initial storage in a text file

# Available user roles
ROLE_OPTIONS = {
    "1": "admin",
    "2": "analytics",
    "3": "cyber",
    "4": "data",
    "5": "it",
    "6": "finance"
}

# Function to hash passwords
def hash_password(password: str) -> bytes:
    """Hashes the password using bcrypt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Function to verify passwords
def verify_password(password: str, hashed: bytes) -> bool:
    """Verifies if the provided password matches the hashed one."""
    return bcrypt.checkpw(password.encode(), hashed)

# Save user details (username, hashed password, and role) to the file
def save_user(username: str, password_hash: bytes, role: str):
    """Saves a new user to the users.txt file."""
    with open(USERS_FILE, "a") as f:
        f.write(f"{username},{password_hash.decode()},{role}\n")

# Load all users from the file
def load_users():
    """Loads all users from the users.txt file."""
    if not os.path.exists(USERS_FILE):
        return {}

    users = {}
    with open(USERS_FILE, "r") as f:
        for line in f:
            username, pwd_hash, role = line.strip().split(",")
            users[username] = {"hash": pwd_hash.encode(), "role": role}
    return users

# Function to register a new user
def register_user():
    """Handles the user registration process."""
    print("\n--- User Registration ---")
    username = input("Enter username: ")
    password = input("Enter password: ")
    confirm_password = input("Confirm password: ")

    if password != confirm_password:
        print("❌ Passwords do not match!")
        return

    print("\nSelect a role:")
    for number, role in ROLE_OPTIONS.items():
        print(f"{number}. {role}")

    role_choice = input("Enter role number: ")
    if role_choice not in ROLE_OPTIONS:
        print("❌ Invalid role number!")
        return

    users = load_users()
    if username in users:
        print("❌ Username already exists!")
        return

    hashed = hash_password(password)
    save_user(username, hashed, ROLE_OPTIONS[role_choice])

    print(f"✅ User '{username}' registered successfully!")
    print(f"🎉 Role assigned: {ROLE_OPTIONS[role_choice]}")

# Function to login a user
def login_user():
    """Handles the user login process."""
    print("\n--- Login ---")
    username = input("Enter username: ")
    password = input("Enter password: ")

    users = load_users()
    if username not in users:
        print("❌ User not found!")
        return

    if verify_password(password, users[username]["hash"]):
        print(f"✅ Login successful! Welcome {username}!")
        print(f"🎉 Role: {users[username]['role']}")
    else:
        print("❌ Incorrect password!")

# Main menu function for user interaction
def main():
    """Main menu for user registration and login."""
    print("Program started!")  # Debugging statement to confirm the script is running
    while True:
        print("\n--- AUTH MENU ---")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            register_user()
        elif choice == "2":
            login_user()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("❌ Invalid choice!")

# Run Program
if __name__ == "__main__":
    main()