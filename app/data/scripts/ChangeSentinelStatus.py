# type: HTTP/Webhook
# path: changeStatus
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

sev = body.get("SentinelSeverity")

link_payload = {
    "open": False,
    "resolution": body.get("SentinelResolution"),
     "state": {
        "severity": sev
    }
}


patch_response = requests.patch(
        url + "/api/tickets/" + body.get("ticketID"),
        headers=header,
        json=link_payload,
        timeout=5)

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