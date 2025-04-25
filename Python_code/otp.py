import requests
import random
import serial.tools.list_ports
import time

generate_no = ''.join(random.choices('0123456789', k=6))
otp=generate_ch+generate_no

# List available serial ports
ports = serial.tools.list_ports.comports()
portsList = [p.device for p in ports]  # Extracting only device names
for p in portsList:
    print(p)

com = input("Select the port for interfacing: ")

if com not in portsList:
    print("Invalid port selection. Exiting...")
    exit()

print(f"------------\n\n{com} is selected")

# Initialize Serial Connection
serialInst = serial.Serial()
serialInst.baudrate = 9600
serialInst.port = com

try:
    serialInst.open()
    time.sleep(2)  # Allow Arduino to reset
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit()

serialInst.write(otp.encode('utf-8'))
print("Sent otp : ",otp)
serialInst.close()
print("Serial communication closed.")

# Define the API endpoint and API key
api_key = "" #your API key
url = "https://www.circuitdigest.cloud/send_sms?ID=101"

# Set the payload with the recipient's mobile number and dynamic variables
payload = {
    "mobiles": "",  # Replace with recipient's mobile number
    "var1": "Smart Lock System",         # Replace with your first variable
    "var2": f"working. Your Pw for unlocking is {otp}" # Replace with your second variable
}

# Set the headers with the API key
headers = {
    "Authorization": api_key,
    "Content-Type": "application/json"
}

# Send the POST request
response = requests.post(url, headers=headers, json=payload)

# Handle the response
if response.status_code == 200:
    print("SMS sent successfully!")
    print("Response:", response.json())
else:
    print("Failed to send SMS. Status code:", response.status_code)
    print("Error:", response.text)