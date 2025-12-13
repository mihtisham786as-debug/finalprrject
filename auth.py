import bcrypt
import os

USERS_FILE = "users.txt"

ROLE_OPTIONS = {
    "1": "admin",
    "2": "analytics",
    "3": "cyber",
    "4": "data",
    "5": "it",
    "6": "finance"1
}

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# Hash Functions
def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed)

# User File Management
def save_user(username: str, password_hash: bytes, role: str):
    with open(USERS_FILE, "a") as f:
        f.write(f"{username},{password_hash.decode()},{role}\n")

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    users = {}
    with open(USERS_FILE, "r") as f:
        for line in f:
            username, pwd_hash, role = line.strip().split(",")
            users[username] = {"hash": pwd_hash.encode(), "role": role}
    return users

# User Registration 
def register_user():
    print(f"\n{YELLOW}--- User Registration ---{RESET}")
    username = input("Enter username: ")
    password = input("Enter password: ")          # visible input for Mac
    confirm_password = input("Confirm password: ")

    if password != confirm_password:
        print(f"{RED}❌ Passwords do not match!{RESET}")
        return

    print("\nSelect a role:")
    for number, role in ROLE_OPTIONS.items():
        print(f"{number}. {role}")

    role_choice = input("Enter role number: ")
    if role_choice not in ROLE_OPTIONS:
        print(f"{RED}❌ Invalid role number!{RESET}")
        return

    role = ROLE_OPTIONS[role_choice]
    users = load_users()
    if username in users:
        print(f"{RED}❌ Username already exists!{RESET}")
        return

    hashed = hash_password(password)
    save_user(username, hashed, role)
    print(f"{GREEN}✅ User '{username}' registered successfully!{RESET}")
    print(f"{GREEN}🎉 Welcome {username} to the {role} department!{RESET}")

# User Login 
def login_user():
    print(f"\n{YELLOW}--- Login ---{RESET}")
    username = input("Enter username: ")
    password = input("Enter password: ")
    users = load_users()
    if username not in users:
        print(f"{RED}❌ User not found!{RESET}")
        return
    stored_hash = users[username]["hash"]
    role = users[username]["role"]
    if verify_password(password, stored_hash):
        print(f"{GREEN}✅ Login successful! Welcome {username}!{RESET}")
        print(f"{GREEN}🎉 Role: {role}{RESET}")
    else:
        print(f"{RED}❌ Incorrect password!{RESET}")

# Main Menu 
def main():
    while True:
        print(f"\n{YELLOW}--- AUTH MENU ---{RESET}")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            register_user()
        elif choice == "2":
            login_user()
        elif choice == "3":
            print(f"{GREEN}Exiting...{RESET}")
            break
        else:
            print(f"{RED}❌ Invalid choice!{RESET}")

# 1Run Program 
if __name__ == "__main__":
    main()
