#!/usr/bin/env python3
"""Tiny web server to check a VM is reachable from the host over a bridged network.

Run on the VM:   python3 server.py          (port 8080)
                 python3 server.py 9000     (any other port)
Open on host:    http://<VM-IP>:8080
"""
import datetime
import http.server
import socket
import subprocess
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080


def vm_ips():
    try:
        return subprocess.check_output(["hostname", "-I"], text=True).split()
    except Exception:
        return [socket.gethostbyname(socket.gethostname())]


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        body = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Bridge test OK</title>
<style>body{{font-family:sans-serif;max-width:600px;margin:60px auto;line-height:1.6}}
h1{{color:#1a7f37}} code{{background:#eee;padding:2px 6px;border-radius:4px}}</style></head>
<body>
<h1>&#10004; It works &mdash; the VM is reachable</h1>
<p><b>VM hostname:</b> <code>{socket.gethostname()}</code></p>
<p><b>VM IP address(es):</b> <code>{', '.join(vm_ips())}</code></p>
<p><b>Your (visitor) IP:</b> <code>{self.client_address[0]}</code></p>
<p><b>Server time:</b> <code>{datetime.datetime.now():%Y-%m-%d %H:%M:%S}</code></p>
</body></html>"""
        data = body.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


if __name__ == "__main__":
    print(f"Serving on port {PORT}. From Windows, open one of:")
    for ip in vm_ips():
        print(f"  http://[{ip}]:{PORT}" if ":" in ip else f"  http://{ip}:{PORT}")
    print("Press Ctrl+C to stop.")
    http.server.ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
