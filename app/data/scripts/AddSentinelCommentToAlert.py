# type: HTTP/Webhook
# path: addCommentToAlert
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

# Create a comment
link_payload = {
    "ticket": body.get("ticketID"),
    "author": "u648db8764ada6a",
    "message": body.get("SentinelMessage")
}

try:
    requests.post(url + "/api/comments", headers=header,
        json=link_payload,
        timeout=5
    )

except Exception as e:
    print("Failed to send ticket info to server:", e)