"""Local server for the proof-translation page: checks Lean and runs Python on this computer.

    python3 server.py            # then open http://127.0.0.1:8765

Lean files are checked with `lake env lean` inside ../lean_upper_bound (needs elan and the
Mathlib cache: run `lake exe cache get` there once). Python runs in a separate python3 process.
Both run code typed into the page, so the server only listens on 127.0.0.1 and only accepts
JSON requests addressed to localhost.
"""
import json, os, re, subprocess, sys, tempfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
LEAN_PROJECT = os.path.normpath(os.path.join(HERE, "..", "lean_upper_bound"))
PORT = int(os.environ.get("PORT", "8765"))
LAKE = os.environ.get("LAKE", os.path.expanduser("~/.elan/bin/lake"))
if not os.path.exists(LAKE):
    LAKE = "lake"


def lean_version():
    try:
        return subprocess.run([LAKE, "env", "lean", "--version"], cwd=LEAN_PROJECT,
                              capture_output=True, text=True, timeout=60).stdout.split(",")[0].replace("Lean (version ", "").strip()
    except Exception as e:
        return "unavailable (%s)" % e


LEAN_VERSION = lean_version()


def run(cmd, code, suffix, cwd, timeout):
    with tempfile.NamedTemporaryFile("w", suffix=suffix, delete=False, dir=cwd if suffix == ".lean" else None) as f:
        f.write(code)
        path = f.name
    try:
        p = subprocess.run(cmd + [path], cwd=cwd, capture_output=True, text=True, timeout=timeout)
        out = (p.stdout + p.stderr).replace(path, os.path.basename(path))
        return p.returncode, out
    except subprocess.TimeoutExpired:
        return 1, "stopped after %d s" % timeout
    finally:
        os.unlink(path)


class Handler(BaseHTTPRequestHandler):
    def _local(self):
        host = (self.headers.get("Host") or "").split(":")[0]
        return host in ("127.0.0.1", "localhost")

    def _send(self, code, body, ctype="application/json"):
        data = body if isinstance(body, bytes) else json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if not self._local():
            return self._send(403, {"error": "localhost only"})
        if self.path in ("/", "/index.html"):
            with open(os.path.join(HERE, "proof_translation.html"), "rb") as f:
                page = f.read()
            shell = (b'<!doctype html><html lang="en"><head><meta charset="utf-8">'
                     b'<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"></head><body>')
            return self._send(200, shell + page + b"</body></html>", "text/html; charset=utf-8")
        if self.path == "/api/health":
            return self._send(200, {"ok": True, "lean": LEAN_VERSION})
        self._send(404, {"error": "not found"})

    def do_POST(self):
        if not self._local() or "application/json" not in (self.headers.get("Content-Type") or ""):
            return self._send(403, {"error": "localhost JSON only"})
        n = int(self.headers.get("Content-Length") or 0)
        code = json.loads(self.rfile.read(n) or b"{}").get("code", "")
        if self.path == "/api/lean":
            rc, out = run([LAKE, "env", "lean"], code, ".lean", LEAN_PROJECT, 600)
            sorry = bool(re.search(r"declaration uses 'sorry'", out))
            return self._send(200, {"ok": rc == 0 and "error" not in out, "sorry": sorry, "output": out.strip()})
        if self.path == "/api/python":
            rc, out = run([sys.executable, "-I"], code, ".py", None, 120)
            return self._send(200, {"ok": rc == 0, "output": out})
        self._send(404, {"error": "not found"})

    def log_message(self, fmt, *args):
        sys.stderr.write("%s\n" % (fmt % args))


if __name__ == "__main__":
    print("Lean:", LEAN_VERSION, "| project:", LEAN_PROJECT)
    print("Open http://127.0.0.1:%d" % PORT)
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
