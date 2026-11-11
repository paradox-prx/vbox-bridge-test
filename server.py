#!/usr/bin/env python3
"""Izhan's Local Server - a tiny web server to check a VM is reachable
from the host over a bridged network. Made by Izhan.

Run on the VM:   python3 server.py          (port 8080)
                 python3 server.py 9000     (any other port)
Open on host:    http://<VM-IP>:8080
Stop:            Ctrl+C
"""
import datetime
import errno
import html
import http.server
import socket
import string
import subprocess
import sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080

PAGE = string.Template("""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Izhan's Local Server // Comms Link Established</title>
<link href="https://fonts.googleapis.com/css2?family=Black+Ops+One&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<style>
:root{--olive:#4b5320;--drab:#2f3318;--khaki:#c3b091;--sand:#e6d8b5;--green:#7cfc00;--red:#c0392b}
*{box-sizing:border-box;margin:0}
body{min-height:100vh;color:var(--sand);font-family:'Share Tech Mono',ui-monospace,monospace;
 background:
  radial-gradient(ellipse 22% 14% at 12% 18%,#3b4220 60%,transparent 61%),
  radial-gradient(ellipse 18% 20% at 78% 12%,#22260f 60%,transparent 61%),
  radial-gradient(ellipse 26% 16% at 60% 70%,#3b4220 60%,transparent 61%),
  radial-gradient(ellipse 16% 22% at 20% 80%,#5a4a2e 60%,transparent 61%),
  radial-gradient(ellipse 20% 12% at 92% 88%,#5a4a2e 60%,transparent 61%),
  radial-gradient(ellipse 14% 18% at 40% 35%,#22260f 60%,transparent 61%),
  var(--olive);
 display:flex;align-items:center;justify-content:center;padding:24px}
.panel{width:100%;max-width:720px;background:rgba(18,20,10,.92);border:2px solid var(--khaki);
 box-shadow:0 0 0 6px rgba(18,20,10,.6),0 20px 60px rgba(0,0,0,.6);position:relative;overflow:hidden}
.panel::after{content:"";position:absolute;inset:0;pointer-events:none;
 background:repeating-linear-gradient(0deg,rgba(255,255,255,.03) 0 1px,transparent 1px 3px)}
.tape{height:14px;background:repeating-linear-gradient(45deg,#e0b300 0 16px,#111 16px 32px)}
.head{display:flex;gap:20px;align-items:center;padding:24px 28px 8px}
.radar{flex:none;width:96px;height:96px;border-radius:50%;border:2px solid var(--green);position:relative;
 background:radial-gradient(circle,transparent 30%,rgba(124,252,0,.15) 31%,transparent 33%,transparent 63%,rgba(124,252,0,.15) 64%,transparent 66%),
  linear-gradient(transparent 49.5%,rgba(124,252,0,.3) 50%,transparent 50.5%),
  linear-gradient(90deg,transparent 49.5%,rgba(124,252,0,.3) 50%,transparent 50.5%),#071003}
.radar::before{content:"";position:absolute;inset:0;border-radius:50%;
 background:conic-gradient(from 0deg,rgba(124,252,0,.55),transparent 70deg);animation:sweep 2.4s linear infinite}
.radar::after{content:"";position:absolute;width:8px;height:8px;border-radius:50%;background:var(--green);
 top:28%;left:62%;box-shadow:0 0 10px var(--green);animation:blip 2.4s ease-out infinite}
@keyframes sweep{to{transform:rotate(360deg)}}
@keyframes blip{0%,15%{opacity:0}20%{opacity:1}100%{opacity:0}}
.classified{display:inline-block;font-family:'Black Ops One',Impact,sans-serif;color:var(--red);border:2px solid var(--red);
 padding:2px 10px;letter-spacing:3px;font-size:.8rem;transform:rotate(-3deg);margin-bottom:8px}
h1{font-family:'Black Ops One',Impact,sans-serif;font-weight:400;font-size:clamp(1.7rem,5vw,2.6rem);
 letter-spacing:2px;color:var(--khaki);text-transform:uppercase;line-height:1.05}
.status{margin:14px 28px 6px;padding:12px 16px;border-left:4px solid var(--green);background:rgba(124,252,0,.08);
 color:var(--green);letter-spacing:2px;text-transform:uppercase;font-size:1.05rem}
.status b{animation:pulse 1.2s steps(2) infinite}
@keyframes pulse{50%{opacity:.25}}
table{width:calc(100% - 56px);margin:16px 28px 24px;border-collapse:collapse}
td{padding:10px 0;border-bottom:1px dashed rgba(195,176,145,.3);vertical-align:top}
td:first-child{width:42%;color:var(--khaki);letter-spacing:2px;font-size:.85rem;text-transform:uppercase}
td:last-child{color:#fff;word-break:break-all}
footer{display:flex;justify-content:space-between;flex-wrap:wrap;gap:6px;padding:12px 28px;
 background:rgba(0,0,0,.35);font-size:.8rem;letter-spacing:2px;text-transform:uppercase;color:var(--khaki)}
footer strong{font-family:'Black Ops One',Impact,sans-serif;font-weight:400;color:var(--sand);letter-spacing:3px}
@media(max-width:520px){.head{flex-direction:column;align-items:flex-start}td:first-child{width:45%}}
</style></head>
<body><div class="panel">
<div class="tape"></div>
<div class="head">
 <div class="radar" aria-hidden="true"></div>
 <div><span class="classified">Top Secret</span><h1>Izhan's Local Server</h1></div>
</div>
<div class="status"><b>&#9632;</b> Comms link established &mdash; target VM reachable</div>
<table>
 <tr><td>Callsign (host)</td><td>$hostname</td></tr>
 <tr><td>Grid ref (VM IP)</td><td>$ips</td></tr>
 <tr><td>Port</td><td>$port</td></tr>
 <tr><td>Contact (your IP)</td><td>$visitor</td></tr>
 <tr><td>Local time</td><td>$local</td></tr>
 <tr><td>Zulu time</td><td>$zulu Z</td></tr>
</table>
<footer><span>Made by <strong>Izhan</strong></span><span>Local server // Ubuntu // Operation Bridge</span></footer>
<div class="tape"></div>
</div></body></html>""")


def vm_ips():
    try:
        return subprocess.check_output(["hostname", "-I"], text=True).split()
    except Exception:
        return [socket.gethostbyname(socket.gethostname())]


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        now = datetime.datetime.now()
        body = PAGE.substitute(
            hostname=html.escape(socket.gethostname()),
            ips="<br>".join(html.escape(ip) for ip in vm_ips()),
            port=PORT,
            visitor=html.escape(self.client_address[0]),
            local=now.strftime("%Y-%m-%d %H:%M:%S"),
            zulu=datetime.datetime.utcnow().strftime("%H%M"),
        )
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
