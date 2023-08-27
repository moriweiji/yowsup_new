import tkinter as tk
from tkinter import filedialog
import pandas as pd
import subprocess
import time
import random

# Function to send messages
def send_messages():
    message = message_entry.get()
    if not message:
        result_label.config(text="Message cannot be empty")
        return

    file_path = file_path_entry.get()
    if not file_path:
        result_label.config(text="Select a file first")
        return

    try:
        df = pd.read_csv(file_path)  # You can use read_excel for Excel files
        phone_numbers = df['Phone Number'].tolist()

        for phone_number in phone_numbers:
            command = f"python yowsup-cli demos --config config.txt -s {phone_number} '{message}'"
            subprocess.call(command, shell=True)
            random_delay = random.uniform(3, 8)
            time.sleep(random_delay)

        result_label.config(text="Messages sent successfully")
    except Exception as e:
        result_label.config(text=f"Error: {str(e)}")

# Create the main window
window = tk.Tk()
window.title("Message Sender")

# Create and place widgets
message_label = tk.Label(window, text="Enter Message:")
message_label.pack()

message_entry = tk.Entry(window)
message_entry.pack()

file_path_label = tk.Label(window, text="Select CSV/Excel File:")
file_path_label.pack()

file_path_entry = tk.Entry(window)
file_path_entry.pack()

file_browse_button = tk.Button(window, text="Browse", command=lambda: file_path_entry.insert(0, filedialog.askopenfilename()))
file_browse_button.pack()

send_button = tk.Button(window, text="Send Messages", command=send_messages)
send_button.pack()

result_label = tk.Label(window, text="")
result_label.pack()

# Start the GUI main loop
window.mainloop()
