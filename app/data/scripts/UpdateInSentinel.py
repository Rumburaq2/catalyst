# type: Collection Hook
# collections: Tickets
# events: Update Events
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

requests.post("https://webhook.site/c0c88054-7b27-4238-8428-9a90b5415e17", json=ticket)

# 1. Parse the initial webhook payload
webhook_event = json.loads(sys.argv[1])
record_from_webhook = webhook_event.get("record", {})
ticket_id = record_from_webhook.get("id")

if not ticket_id:
    print("Error: No ticket ID found in the webhook payload.")
    sys.exit(1)

# 2. THE FIX: Fetch the authoritative, complete ticket data from the API
try:
    print(f"Fetching full data for ticket {ticket_id}...")
    api_response = requests.get(f"{url}/api/tickets/{ticket_id}", headers=header, timeout=5)
    api_response.raise_for_status()
    
    # This is your true, complete ticket data
    full_ticket_data = api_response.json()
    
except Exception as e:
    print(f"Failed to fetch full ticket data: {e}")
    sys.exit(1)

# 3. Now extract your state safely from the FULL data
ticket_state = full_ticket_data.get("state", {})
arm_id = ticket_state.get("ARM_id")

print(f"Successfully retrieved ARM_id: {arm_id}")

# 4. (Optional) Send to webhook.site to verify it works
requests.post(
    "https://webhook.site/c0c88054-7b27-4238-8428-9a90b5415e17", 
    json={"original_webhook": webhook_event, "fetched_data": full_ticket_data}
)

requests.post(
    "https://webhook.site/c0c88054-7b27-4238-8428-9a90b5415e17", 
    json={"bruh_state": ticket_state}
)



requests.post("https://prod-24.northeurope.logic.azure.com:443/workflows/39e1f4f43b0d41e693f6e192c1a7badd/triggers/When_an_HTTP_request_is_received/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2FWhen_an_HTTP_request_is_received%2Frun&sv=1.0&sig=1WakSF5_lMi06E2g623s3-YHX938kUiPLuhuKpTYPzE", json=ticket)

requests.post("https://webhook.site/c0c88054-7b27-4238-8428-9a90b5415e17", json=ticket)

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
