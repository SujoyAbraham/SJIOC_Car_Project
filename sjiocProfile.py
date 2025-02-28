import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
from tkinter import scrolledtext
import os
import csv

fileLocation = "./files/credentials.txt"

# Generate a key for encryption and decryption
# In a real-world scenario, this key should be securely stored, not hardcoded
def generate_key():
    return Fernet.generate_key()

# Encrypt password before saving to a file
def encrypt_password(password, key):
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password

# Decrypt password when verifying login
def decrypt_password(encrypted_password, key):
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_password).decode()
    return decrypted_password

# Check if user exists in the credentials file
def user_exists(username):
    if not os.path.exists(fileLocation):
        return False
    with open(fileLocation, "r") as file:
        for line in file:
            stored_username, _ = line.strip().split(":")
            if stored_username == username:
                return True
    return False

# Save new user credentials (username and encrypted password)
def save_user(username, encrypted_password):
    with open(fileLocation, "a") as file:
        file.write(f"{username}:{encrypted_password.decode()}\n")

# Verify login credentials
def verify_login(username, password, key):
    if not os.path.exists(fileLocation):
        return False
    with open(fileLocation, "r") as file:
        for line in file:
            stored_username, stored_encrypted_password = line.strip().split(":")
            if stored_username == username:
                decrypted_password = decrypt_password(stored_encrypted_password.encode(), key)
                if decrypted_password == password:
                    return True
    return False

# Register function for creating a new account
def register():
    username = entry_username.get()
    password = entry_password.get()

    if username == "" or password == "":
        messagebox.showwarning(" Register Input Error", "Username and password cannot be empty.")
        return

    if user_exists(username):
        messagebox.showwarning("Username Taken", "This username is already taken. Please choose a different one.")
    else:
        encrypted_password = encrypt_password(password, key)
        save_user(username, encrypted_password)
        messagebox.showinfo("Registration Successful", f"Account for {username} created successfully.")
        switch_to_login()

# Login function to verify credentials
def login():
    username = entry_username.get()
    password = entry_password.get()

    if username == "" or password == "":
        messagebox.showwarning("Input Error", "Username and password cannot be empty.")
        return

    if verify_login(username, password, key):
        messagebox.showinfo("Login Successful", f"Welcome, {username}!")
        # Switch to the chatbot UI or other main functionality here
        switch_to_chatbot()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

# Function to switch to the registration screen
def switch_to_register():
    login_frame.pack_forget()
    register_frame.pack()

# Function to switch to the login screen
def switch_to_login():
    register_frame.pack_forget()
    login_frame.pack()

# Function to switch to the chatbot UI after successful login
def switch_to_chatbot():
    login_frame.pack_forget()
    chatbot_frame.pack()

# Creating the main window
root = tk.Tk()
root.title("Car Search Chatbot - Authentication")
root.geometry("400x400")

# Encryption Key
key = generate_key()

# Login Frame
login_frame = tk.Frame(root)
login_frame.pack(pady=20)

label_username = tk.Label(login_frame, text="Username:")
label_username.grid(row=0, column=0)
entry_username = tk.Entry(login_frame, width=25)
entry_username.grid(row=0, column=1)

label_password = tk.Label(login_frame, text="Password:")
label_password.grid(row=1, column=0)
entry_password = tk.Entry(login_frame, width=25, show="*")
entry_password.grid(row=1, column=1)

login_button = tk.Button(login_frame, text="Login", command=login)
login_button.grid(row=2, column=0, columnspan=2, pady=10)

register_link = tk.Button(login_frame, text="Create an Account", command=switch_to_register)
register_link.grid(row=3, column=0, columnspan=2)

# Register Frame
register_frame = tk.Frame(root)

label_username_reg = tk.Label(register_frame, text="Username:")
label_username_reg.grid(row=0, column=0)
entry_username_reg = tk.Entry(register_frame, width=25)
entry_username_reg.grid(row=0, column=1)

label_password_reg = tk.Label(register_frame, text="Password:")
label_password_reg.grid(row=1, column=0)
entry_password_reg = tk.Entry(register_frame, width=25, show="*")
entry_password_reg.grid(row=1, column=1)

register_button = tk.Button(register_frame, text="Register", command=register)
register_button.grid(row=2, column=0, columnspan=2, pady=10)

back_to_login_link = tk.Button(register_frame, text="Back to Login", command=switch_to_login)
back_to_login_link.grid(row=3, column=0, columnspan=2)

# Chatbot Frame (Placeholder)
chatbot_frame = tk.Frame(root)

#label_chatbot = tk.Label(chatbot_frame, text="Welcome to the Car Search Chatbot!", font=("Arial", 14))
#label_chatbot.pack(pady=50)


# Function to load data from a CSV file
def load_car_data(csv_file):
    cars = []
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cars.append(row)
    return cars

# Dummy function to simulate chatbot responses based on CSV data
def chatbot_response(user_input, car_data):
    # Search for car in the dataset based on the user's input (case-insensitive)
    for car in car_data:
        if user_input.lower() in car['firstname'].lower() or user_input.lower() in car['lastname'].lower() or user_input.lower() in car['carplate'].lower() or user_input.lower() in car['phoneno'].lower():
            # Return car details if a match is found
            response = f"Here are the details for {car['firstname']}:\n" \
                       f"Last Name: {car['lastname']}\n" \
                       f"Phone Number: {car['phoneno']}\n" \
                       f"Car Plate No#: {car['carplate']}\n"
            return response
    return "Sorry, I couldn't find any cars matching your query."

# Function to send user input and get the bot's response
def send_message():
    user_input = user_input_box.get()

    if user_input != "" and user_input != "Enter here":
        # Display the user's message in the chat window
        chat_window.config(state=tk.NORMAL)  # Enable editing the chat window
        chat_window.insert(tk.END, f"You: {user_input}\n")
        chat_window.insert(tk.END, "Bot: " + chatbot_response(user_input, car_data) + "\n\n")
        chat_window.config(state=tk.DISABLED)  # Disable editing the chat window

        user_input_box.delete(0, tk.END)  # Clear the input box after sending the message
        chat_window.yview(tk.END)  # Auto-scroll to the bottom

# Function to handle the placeholder behavior
def on_focus_in(event):
    if user_input_box.get() == "Enter here":
        user_input_box.delete(0, tk.END)  # Clear the placeholder when focused
        user_input_box.config(fg="black")  # Change text color to black

def on_focus_out(event):
    if user_input_box.get() == "":
        user_input_box.insert(0, "Enter here")  # Insert the placeholder text
        user_input_box.config(fg="gray")  # Change text color to gray

# Set up the main window
root = tk.Tk()
root.title("Car Search Chatbot")
root.geometry("400x500")

# Load car data from CSV
csv_file = "./files/cars.csv"  # Path to your CSV file
car_data = load_car_data(csv_file)

# Create a frame for the chat window
chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20, font=("Arial", 12))
chat_window.grid(row=0, column=0, padx=10, pady=10)
chat_window.config(state=tk.DISABLED)  # Make the chat window read-only

# Create an entry box for the user to type messages
user_input_box = tk.Entry(root, width=40, font=("Arial", 12))
user_input_box.grid(row=1, column=0, padx=10, pady=10)

# Add placeholder text ("Enter here")
user_input_box.insert(0, "Enter here")  # Insert placeholder
user_input_box.config(fg="gray")  # Set placeholder text color to gray

# Bind the focus events to handle placeholder behavior
user_input_box.bind("<FocusIn>", on_focus_in)
user_input_box.bind("<FocusOut>", on_focus_out)

# Create a button to send the message
send_button = tk.Button(root, text="Send", font=("Arial", 12), command=send_message)
send_button.grid(row=2, column=0, padx=10, pady=10)

# Run the Tkinter event loop
# Run the application
root.mainloop()
