# Opaige for Python

The Opaige API from Python 3.8 or later. Standard library only.

```python
import os
from opaige import Opaige, OpaigeError, verify_webhook

opaige = Opaige(os.environ["OPAIGE_KEY"])

answer = opaige.check_requirements(passport="IN", destination="FR")

opaige.send_bookings(body={"bookings": [{
    "ref": "QX7K2M", "flight": {"number": "OP412", "destination": "GB", "depart_date": "2026-12-18"},
    "passengers": [{"ref": "QX7K2M-1", "passport": "IN", "residence": "AE"}],
}]})

review = opaige.review_file(file=pdf_bytes, fields={"destination": "FR", "purpose": "business"}, idempotency_key="file-8841")
```

Every method is one API call, named as in the [API reference](https://opaige.com/developers), in snake_case. JSON goes in `body`;
a PDF comes back as `bytes`. A query value that is a Python word gets an underscore: `list_invoices(from_="2026-10-01")`.

**Errors** raise `OpaigeError` with `status`, `code`, `request_id` (quote it to support) and `details`.
**Retries:** reads, and writes sent with an `idempotency_key`, are tried again after 429 and 5xx answers (`max_retries`, default 2).
**Sandbox:** a sandbox key answers in the same shape, is never billed and never touches live data. Bookings, students and appointments it sends are kept as test data.

## Webhooks

```python
event = verify_webhook(request.get_data(), request.headers.get("Opaige-Signature"), os.environ["OPAIGE_WEBHOOK_SECRET"])
```

Pass the raw body: a parsed and re-serialised body no longer matches its signature.
