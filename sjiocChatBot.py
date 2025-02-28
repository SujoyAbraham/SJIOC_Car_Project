import tkinter as tk
from tkinter import scrolledtext
import csv

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
root.mainloop()
