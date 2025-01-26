import requests

BASE_URL = "http://127.0.0.1:5000/api/chat"

# Prompt the user for inputs
user_id = input("Enter your User ID (optional, leave blank if not logged in): ")
user_message = input("Enter your query for the virtual assistant: ")

# Create the payload with the user data and message
payload = {
    "user_id": user_id if user_id else None,  # Set user_id to None if not logged in
    "message": user_message,
}

# Send the request to the chat endpoint
response = requests.post(BASE_URL, json=payload)

# Print the server's response
print("Server Response:")
print(response.json())
