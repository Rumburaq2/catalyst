# type: HTTP/Webhook
# path: webhook
# requirements.txt
# requests
#
import sys
import json
import random
import os

import requests

# Parse the event from the webhook payload
event = json.loads(sys.argv[1])
body = json.loads(event["body"])

url = os.environ["CATALYST_APP_URL"]
header = {"Authorization": "Bearer " + os.environ["CATALYST_TOKEN"]}

# Get data for alert creation
ticket_payload = {
    "name": body.get("name"),
    "description": body.get("description"),
    "type": "alert",
    "open": True,
    "state": body.get("state", {}),
    "IncidentArmId": body.get("IncidentArmId"),
    "IncidentURL": body.get("IncidentURL")
}

# the request will create the alert
response = requests.post(url + "/api/tickets", headers=header, json=ticket_payload)
# Capture Catalyst's response safely
try:
    catalyst_response_data = response.json()
except Exception:
    catalyst_response_data = {"raw_response": response.text}

#now we need to concat the incident ARM id and URL to the existing server response
if isinstance(catalyst_response_data, dict):
    catalyst_response_data["IncidentArmId"] = body.get("IncidentArmId")
    catalyst_response_data["IncidentURL"] = body.get("IncidentURL")

# Forward Catalyst’s response to Logic App Catalyst-AddTag
try:
    forward_response = requests.post(
        "https://prod-45.northeurope.logic.azure.com:443/workflows/b545653657ad4f7fbc4072f1c472c4b1/triggers/When_an_HTTP_request_is_received/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2FWhen_an_HTTP_request_is_received%2Frun&sv=1.0&sig=jtBGrjzE7zgbF6Irpi9oPIAxYWAkv9gvxaljPWsWvGQ",
        json= catalyst_response_data,
        timeout=5
    )
    forward_response.raise_for_status()

    try:
        print("Local server response:", forward_response.json())
    except Exception:
        print("Local server raw response:", forward_response.text)

except Exception as e:
    print("Failed to send ticket info to server:", e)