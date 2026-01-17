# type: HTTP/Webhook
# path: changeOwner
# requirements.txt
# requests
#
import sys
import json
import random
import os
import requests

url = os.environ["CATALYST_APP_URL"]
header = {"Authorization": "Bearer " + os.environ["CATALYST_TOKEN"]}

event = json.loads(sys.argv[1])
body = json.loads(event["body"])

lookingForUser = body.get("SentinelOwner")
sev = body.get("SentinelSeverity")
ticketID = body.get("ticketID")

# Get All Users
users = requests.get(url + "/api/users", headers=header).json()

# Find the Specific User ID
# We look for a user whose 'email' matches the 'SentinelOwner' variable.
target_user = next((u for u in users if u["email"] == lookingForUser), None)

if target_user:
    user_id_to_assign = target_user["id"]
else:
    # Fallback: If no match found, pick a random user (or handle error)
    random_user = random.choice(users)
    user_id_to_assign = random_user["id"]

link_payload = {
    "owner": user_id_to_assign,
    "state": {
        "severity": sev
    }
}

# Assign the ticket to the user from Sentinel
patch_response = requests.patch(
    url + "/api/tickets/" + ticketID,
    headers=header,
    json=link_payload
)

# Send the ticket data to your local HTTP server
try:
    response = requests.post(
        "http://127.0.0.1:8001",
        json=patch_response.text,
        timeout=5
    )
    response.raise_for_status()
    print("Sent ticket info to server successfully:", response.json())
except Exception as e:
    print("Failed to send ticket info to server:", e)