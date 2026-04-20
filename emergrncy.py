import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

file_path = r"C:\ProgramData\SecureApp\data.enc"


def encrypt(text, key):
    key = key.ljust(16)[:16].encode()
    cipher = AES.new(key, AES.MODE_CBC)
    encrypted = cipher.encrypt(pad(text.encode(), AES.block_size))
    return cipher.iv + encrypted


def decrypt(enc_data, key):
    key = key.ljust(16)[:16].encode()
    iv = enc_data[:16]
    ciphertext = enc_data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext), AES.block_size).decode()


if not os.path.exists(file_path):
    open(file_path, "wb").close()

while True:
    print("\n1. Store Data")
    print("2. View Data")
    print("3. Exit")

    choice = input("Enter choice: ")

    
    if choice == '1':
        username = input("Enter username: ")

        if not username.isalpha():
            print("Username must contain only alphabets!")
            continue

        data = input("Enter data: ")
        key = input("Enter secret key: ")

        encrypted = encrypt(data, key)

        # Store: username|encrypted_data
        with open(file_path, "ab") as file:
            file.write(username.encode() + b"|")
            file.write(encrypted + b"\n")

        print("Data stored securely in binary file!")

    elif choice == '2':
        search_user = input("Enter username: ")

        if not search_user.isalpha():
            print(" Username must contain only alphabets!")
            continue

        user_key = input("Enter secret key: ")
        found = False

        try:
            with open(file_path, "rb") as file:
                lines = file.readlines()

                for line in lines:
                    try:
                        username, enc_data = line.split(b"|", 1)
                        enc_data = enc_data.strip()

                        if username.decode().lower() == search_user.lower():
                            decrypted = decrypt(enc_data, user_key)
                            print(" Decrypted Data:", decrypted)
                            found = True
                            break
                    except:
                        continue

            if not found:
                print("Username not found or wrong key!")

        except FileNotFoundError:
            print("File not found!")

    elif choice == '3':
        print("Exiting...")
        break

    else:
        print("Invalid choice")
