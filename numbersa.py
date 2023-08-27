import subprocess
import time

# List of phone numbers to send the message to
phone_numbers = [
    "916204556171",
    "918732999707",
    "919755359150"
    # Add more phone numbers here
]

message = "HI guys"

for phone_number in phone_numbers:
    command = f"python yowsup-cli demos --config config.txt -s {phone_number} '{message}' "
    subprocess.call(command, shell=True)
    
    # Add a 10-second delay
    time.sleep(5)
