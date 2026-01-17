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
