# type: HTTP/Webhook
# path: addSentinelURLtoAlert
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

# Parse the event from the webhook payload
event = json.loads(sys.argv[1])
body = json.loads(event["body"])

# Extract the existing state or create an empty dictionary
ticket_state = body.get("state", {})

# Add custom ARM_id to the state dictionary
ticket_state["ARM_id"] = body.get("IncidentARM_ID")
ticket_state["severity"] = body.get("IncidentSev")

# Get data for alert creation
ticket_payload = {
    "state": ticket_state
}

ticketID = body.get("ticketID")

#link_payload = {
#    "ARM_id": body.get("IncidentARM_ID"),
#}

patch_response = requests.patch(
    url + "/api/tickets/" + ticketID,
    headers=header,
    json=ticket_payload
)

response_data = patch_response.json()

#requests.post("https://webhook.site/c84ee3e3-04bd-4626-aa29-27844c8b14b3", #json=response_data)

# Create a Link
link_payload = {
    "ticket": body.get("ticketID"),
    "name": "Link to incident",
    "url": body.get("IncidentURL")
}

#
try:
    requests.post(url + "/api/links", headers=header,
        json=link_payload,
        timeout=5
    )

except Exception as e:
    print("Failed to send ticket info to server:", e)
