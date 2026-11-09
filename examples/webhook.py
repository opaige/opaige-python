"""Verifying a webhook, offline: signs a sample delivery with a test secret, then checks it the way your endpoint will.

    python examples/webhook.py
"""
import hashlib
import hmac
import json
import time

from opaige import verify_webhook

secret = "whsec_example_only"
raw = json.dumps({"event": "lodgement.updated", "data": {"lodgement_id": "lg_example", "status": "submitted"}})
t = int(time.time())
signature = f"t={t},v1=" + hmac.new(secret.encode(), f"{t}.{raw}".encode(), hashlib.sha256).hexdigest()

event = verify_webhook(raw, signature, secret)  # pass the RAW body, exactly as received
print("Verified:", event["event"], event["data"]["status"])

try:
    verify_webhook(raw.replace("submitted", "changed"), signature, secret)
except Exception as e:
    print("A changed body is refused:", e)
