"""How every call is made: the key, the JSON or the file, retries and errors. Written by hand; the API methods beside it
(operations.py) are generated from the API description. Standard library only."""
import json
import time
import uuid
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, Optional

VERSION = "2.0.0"
_RETRY = {429, 500, 502, 503, 504}


class OpaigeError(Exception):
    def __init__(self, message: str, status: int, code: Optional[str] = None, request_id: Optional[str] = None, details: Any = None):
        super().__init__(message)
        self.status, self.code, self.request_id, self.details = status, code, request_id, details


class Requester:
    def __init__(self, key: str, base_url: str = "https://opaige.com/api/company/v1", timeout: float = 120.0, max_retries: int = 2):
        if not key:
            raise ValueError("An Opaige API key is required: create one in the portal under Developers.")
        self._key, self._base, self._timeout, self._retries = key, base_url.rstrip("/"), timeout, max_retries

    def request(self, method: str, path: str, query: Optional[Dict[str, Any]] = None, body: Any = None,
                file: Optional[bytes] = None, filename: str = "file.pdf", fields: Optional[Dict[str, str]] = None,
                idempotency_key: Optional[str] = None) -> Any:
        q = {k: v for k, v in (query or {}).items() if v is not None and v != ""}
        url = self._base + path + ("?" + urllib.parse.urlencode(q) if q else "")
        headers = {"Authorization": f"Bearer {self._key}", "User-Agent": f"opaige-python/{VERSION}", "Accept": "application/json"}
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        data = None
        if file is not None:
            boundary = "opaige" + uuid.uuid4().hex
            parts = [f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode() for k, v in (fields or {}).items()]
            parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{filename}"\r\nContent-Type: application/pdf\r\n\r\n'.encode() + file + b"\r\n")
            data = b"".join(parts) + f"--{boundary}--\r\n".encode()
            headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
        elif body is not None:
            data = json.dumps(body).encode()
            headers["Content-Type"] = "application/json"
        retryable = method == "GET" or bool(idempotency_key)
        attempt = 0
        while True:
            req = urllib.request.Request(url, data=data, headers=headers, method=method)
            try:
                with urllib.request.urlopen(req, timeout=self._timeout) as res:
                    raw = res.read()
                    if "application/pdf" in (res.headers.get("Content-Type") or ""):
                        return raw
                    return json.loads(raw or b"{}")
            except urllib.error.HTTPError as e:
                if e.code in _RETRY and retryable and attempt < self._retries:
                    wait = e.headers.get("Retry-After")
                    time.sleep(min(float(wait), 30.0) if wait and wait.replace(".", "", 1).isdigit() else 0.5 * 2 ** attempt)
                    attempt += 1
                    continue
                try:
                    out = json.loads(e.read() or b"{}")
                except ValueError:
                    out = {}
                raise OpaigeError(out.get("error") or f"Opaige answered {e.code}", e.code, out.get("code"), e.headers.get("Opaige-Request-Id"), out.get("details")) from None
            except urllib.error.URLError as e:
                if retryable and attempt < self._retries:
                    time.sleep(0.5 * 2 ** attempt)
                    attempt += 1
                    continue
                raise OpaigeError(f"Could not reach Opaige: {e.reason}", 0, "network_error") from None
