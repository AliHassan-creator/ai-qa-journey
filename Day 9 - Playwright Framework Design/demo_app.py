"""Tiny local API + UI demo for practicing API-created-data/UI-verification."""

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from itertools import count
from urllib.parse import urlparse


class DemoHandler(BaseHTTPRequestHandler):
    records = {}
    next_id = count(1)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/health":
            self._send_json(200, {"status": "ok"})
            return

        if path.startswith("/api/records/"):
            record_id = path.rsplit("/", 1)[-1]
            record = self.records.get(record_id)
            if record is None:
                self._send_json(404, {"error": "Record not found"})
            else:
                self._send_json(200, record)
            return

        if path.startswith("/records/"):
            record_id = path.rsplit("/", 1)[-1]
            page = f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>Record details</title></head>
<body>
  <main>
    <h1>Record details</h1>
    <p id="status" role="status">Loading record...</p>
    <dl id="record" hidden>
      <dt>Record ID</dt><dd data-test="record-id"></dd>
      <dt>Title</dt><dd data-test="record-title"></dd>
      <dt>Description</dt><dd data-test="record-description"></dd>
    </dl>
  </main>
  <script>
    fetch('/api/records/{record_id}')
      .then(async response => {{
        if (!response.ok) throw new Error('Record could not be loaded');
        return response.json();
      }})
      .then(record => {{
        document.querySelector('[data-test="record-id"]').textContent = record.id;
        document.querySelector('[data-test="record-title"]').textContent = record.title;
        document.querySelector('[data-test="record-description"]').textContent = record.description;
        document.querySelector('#record').hidden = false;
        document.querySelector('#status').textContent = 'Record loaded';
      }})
      .catch(error => {{ document.querySelector('#status').textContent = error.message; }});
  </script>
</body>
</html>"""
            self._send(200, page.encode("utf-8"), "text/html; charset=utf-8")
            return

        self._send_json(404, {"error": "Not found"})

    def do_POST(self):
        if urlparse(self.path).path != "/api/records":
            self._send_json(404, {"error": "Not found"})
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(content_length))
        except (ValueError, json.JSONDecodeError):
            self._send_json(400, {"error": "Request body must be valid JSON"})
            return

        title = payload.get("title") if isinstance(payload, dict) else None
        description = payload.get("description") if isinstance(payload, dict) else None
        if not isinstance(title, str) or not title.strip():
            self._send_json(400, {"error": "title is required"})
            return
        if not isinstance(description, str) or not description.strip():
            self._send_json(400, {"error": "description is required"})
            return

        record_id = str(next(self.next_id))
        record = {
            "id": record_id,
            "title": title.strip(),
            "description": description.strip(),
        }
        self.records[record_id] = record
        self._send_json(201, record)

    def _send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self._send(status, body, "application/json; charset=utf-8")

    def _send(self, status, body, content_type):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, _format, *_args):
        """Keep test output focused; this server is only for local practice."""
        _ = (_format, _args)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), DemoHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
