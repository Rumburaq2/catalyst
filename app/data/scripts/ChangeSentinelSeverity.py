# type: HTTP/Webhook
# path: changeSevAlert
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

# Create a severity

# Assign the sev
#requests.patch(url + "/api/tickets/" + body.get("ticketID"), headers=header, json={
#   "state": {
#        "severity": severity
#   }
#})

link_payload = {
    "state": {
        "severity": body.get("SentinelSeverity")
    }
}

try:
    requests.patch(
        url + "/api/tickets/" + body.get("ticketID"),
        headers=header,
        json=link_payload,
        timeout=5
    )
except Exception as e:
    print("Failed to send ticket info to server:", e)