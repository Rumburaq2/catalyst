# type: Collection Hook
# collections: Tickets
# events: Create Events
# requirements.txt
# requests
#
import sys
import json
import random
import os

import requests

# Parse the ticket from the input
ticket = json.loads(sys.argv[1])

url = os.environ["CATALYST_APP_URL"]
header = {"Authorization": "Bearer " + os.environ["CATALYST_TOKEN"]}

try:
    print("Sending data to webhook.site...")
    webhook_response = requests.post(
        "https://webhook.site/c0c88054-7b27-4238-8428-9a90b5415e17", 
        json=ticket,
        timeout=5
    )
    
    # This forces Python to raise an exception if the status code is 4xx or 5xx
    webhook_response.raise_for_status() 
    
    # If it works, print the success
    print(f"Webhook.site Success! Status Code: {webhook_response.status_code}")

except requests.exceptions.HTTPError as err:
    # This catches HTTP errors (like 400 or 500)
    print(f"Webhook.site HTTP Error: {err}")
    print(f"Webhook.site Error Body: {webhook_response.text}")
except Exception as e:
    # This catches network errors, timeouts, etc.
    print(f"Webhook.site Request Failed entirely: {e}")

# Extract the existing state or create an empty dictionary
record = ticket.get("record", {})
ticket_state = record.get("state", {})
alert_schema = ticket_state.get("schema", {})

# Get data for alert creation
ticket_payload = {
    "name": record.get("name"),
    "description": record.get("description"),
    "type": "alert",
    "open": True,
    "state": ticket_state,
    "schema": alert_schema
}

requests.post("https://webhook.site/c0c88054-7b27-4238-8428-9a90b5415e17", json=ticket_payload, timeout=5)

try:
    forward_response = requests.post(
        "https://prod-45.northeurope.logic.azure.com:443/workflows/b545653657ad4f7fbc4072f1c472c4b1/triggers/When_an_HTTP_request_is_received/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2FWhen_an_HTTP_request_is_received%2Frun&sv=1.0&sig=jtBGrjzE7zgbF6Irpi9oPIAxYWAkv9gvxaljPWsWvGQ",
        json=ticket_payload,
        timeout=5
    )
    forward_response.raise_for_status()

    try:
        print("Local server response:", forward_response.json())
    except Exception:
        print("Local server raw response:", forward_response.text)

except Exception as e:
    print("Failed to send ticket info to server:", e)
