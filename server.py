#!/usr/bin/env python3
"""Izhan's Local Server - a tiny web server to check a VM is reachable
from the host over a bridged network. Made by Izhan.

Run on the VM:   python3 server.py          (port 9000)
                 python3 server.py 8080     (any other port)
Open on host:    http://<VM-IP>:9000
"""
import datetime
import errno
import http.server
import socket
import subprocess
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 9000


def vm_ips():
    try:
        return subprocess.check_output(["hostname", "-I"], text=True).split()
    except Exception:
        return [socket.gethostbyname(socket.gethostname())]


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        body = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Izhan's Local Server</title>
<style>body{{font-family:sans-serif;max-width:600px;margin:60px auto;line-height:1.6}}
h1{{margin-bottom:0}} .ok{{color:#1a7f37;font-size:1.2em;margin-top:4px}}
code{{background:#eee;padding:2px 6px;border-radius:4px}}
footer{{margin-top:40px;color:#777;font-size:.9em;border-top:1px solid #ddd;padding-top:12px}}</style></head>
<body>
<h1>Izhan's Local Server</h1>
<p class="ok">&#10004; It works &mdash; the VM is reachable over the network</p>
<p><b>VM hostname:</b> <code>{socket.gethostname()}</code></p>
<p><b>VM IP address(es):</b> <code>{', '.join(vm_ips())}</code></p>
<p><b>Your (visitor) IP:</b> <code>{self.client_address[0]}</code></p>
<p><b>Server time:</b> <code>{datetime.datetime.now():%Y-%m-%d %H:%M:%S}</code></p>
<footer>Made by Izhan &middot; local server running on Ubuntu</footer>
</body></html>"""
        data = body.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


class Server(http.server.ThreadingHTTPServer):
    allow_reuse_address = True  # restart instantly on the same port after stopping
    daemon_threads = True       # open connections never block Ctrl+C


if __name__ == "__main__":
    try:
        server = Server(("0.0.0.0", PORT), Handler)
    except OSError as e:
        if e.errno == errno.EADDRINUSE:
            print(f"Port {PORT} is already in use by another program.")
            print(f"  See what it is:   sudo lsof -i :{PORT}")
            print(f"  Free the port:    sudo fuser -k {PORT}/tcp")
            print(f"  Or use another:   python3 server.py {PORT + 1}")
            sys.exit(1)
        raise

    print("Izhan's Local Server - made by Izhan")
    print(f"Serving on port {PORT}. From Windows, open one of:")
    for ip in vm_ips():
        print(f"  http://[{ip}]:{PORT}" if ":" in ip else f"  http://{ip}:{PORT}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        print("\nServer stopped. Port", PORT, "is free.")
