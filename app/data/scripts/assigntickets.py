import sys
import json
import random
import os
import requests

# Parse the ticket from the input
ticket = json.loads(sys.argv[1])

# Send the ticket data to your local HTTP server
try:
    response = requests.post(
        "http://127.0.0.1:8001",
        json=ticket,
        timeout=5
    )
    response.raise_for_status()
    print("Sent ticket info to server successfully:", response.json())
except Exception as e:
    print("Failed to send ticket info to server:", e)

url = os.environ["CATALYST_APP_URL"]
header = {"Authorization": "Bearer " + os.environ["CATALYST_TOKEN"]}

# Get a random user
users = requests.get(url + "/api/users", headers=header).json()
random_user = random.choice(users)

# Assign the ticket to the random user
requests.patch(url + "/api/tickets/" + ticket["record"]["id"], headers=header, json={
    "owner": random_user["id"]
})