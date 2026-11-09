"""Quickstart: three calls, nothing saved, nothing billed.

    pip install opaige
    python examples/quickstart.py

Uses the public test key unless OPAIGE_KEY is set. Fictional passengers only.
"""
import os

from opaige import Opaige, OpaigeError

opaige = Opaige(os.environ.get("OPAIGE_KEY", "opco_public_test_key"))

# 1. What does a Nigerian passport need for a visit to Germany?
answer = opaige.check_requirements(passport="NG", destination="DE")
print(f"NG -> DE: {answer['visa']['level']}. {answer['visa']['reason']}")

# 2. Who on this flight needs a visa, and by when to file?
check = opaige.check_passengers(body={
    "flight": {"destination": "GB", "depart_date": "2027-03-12"},
    "passengers": [{"ref": "14A", "passport": "CN"}, {"ref": "14B", "passport": "IE"}],
})
for p in check["passengers"]:
    print(f"Seat {p['ref']} ({p['passport']}): {p['status']}")

# 3. Errors carry a status, a code to branch on, and a request id to quote to support.
try:
    opaige.create_trip(body={})  # the public test key may not plan trips
except OpaigeError as e:
    print(f"Refused as expected: {e.status} {e.code} ({e}) request {e.request_id}")
