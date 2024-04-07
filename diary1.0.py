from cryptography.fernet import Fernet
import os

# Generate a key for encryption
def generate_key():
    return Fernet.generate_key()

# Load the key from a file or generate a new one if it doesn't exist
def load_key():
    key_file = "key.key"
    if os.path.exists(key_file):
        with open(key_file, "rb") as file:
            return file.read()
    else:
        key = generate_key()
        with open(key_file, "wb") as file:
            file.write(key)
        return key

# Encrypt data using the key
def encrypt_message(message, key):
    cipher_suite = Fernet(key)
    return cipher_suite.encrypt(message.encode())

# Decrypt data using the key
def decrypt_message(encrypted_message, key):
    cipher_suite = Fernet(key)
    return cipher_suite.decrypt(encrypted_message).decode()

def main():
    key = load_key()
    print("Welcome to your diary!")

    while True:
        action = input("Would you like to read, write, or quit? ").lower()

        if action == "write":
            entry = input("Write your entry: ")
            encrypted_entry = encrypt_message(entry, key)
            with open("diary.txt", "ab") as file:
                file.write(encrypted_entry + b"\n")
            print("Entry saved.")

        elif action == "read":
            try:
                with open("diary.txt", "rb") as file:
                    for line in file:
                        decrypted_entry = decrypt_message(line.strip(), key)
                        print(decrypted_entry)
            except FileNotFoundError:
                print("No entries found.")

        elif action == "quit":
            print("Goodbye!")
            break

        else:
            print("Invalid action. Please choose write, read, or quit.")

if __name__ == "__main__":
    main()
