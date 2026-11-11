# Izhan's Local Server (vbox-bridge-test)

Made by Izhan. A one-file Python web server for checking that a VirtualBox (or VMware) VM on a
**bridged network adapter** can be reached from the host machine.

No dependencies. It only needs `python3`, which Ubuntu already has.

## 1. Set the VM to bridged networking

VirtualBox → VM **Settings → Network → Adapter 1**:
- **Attached to:** `Bridged Adapter`
- **Name:** your host's active network card (Wi-Fi or Ethernet)

Start the VM. It should now get an IP address on the same network as the host.

## 2. Run the server on the VM (Ubuntu)

```bash
wget https://raw.githubusercontent.com/paradox-prx/vbox-bridge-test/main/server.py
python3 server.py
```

It prints the URL(s) to open, for example:

```
Izhan's Local Server - made by Izhan
Serving on port 9000. From Windows, open one of:
  http://192.168.1.45:9000
```

Default port is 9000. Use a different one with `python3 server.py 8080`.

## 3. Open it from Windows

Open the printed URL in a browser on the host. A green **"It works"** page means the
bridge is working. The page also shows the VM's IP and your visitor IP.

## Troubleshooting

| Symptom | Fix |
|---|---|
| VM IP starts with `10.0.2.` | The adapter is still on NAT. Switch it to Bridged Adapter and run `sudo dhclient -r && sudo dhclient` or reboot the VM. |
| Page doesn't load, but the VM's own browser loads `http://localhost:9000` | The Ubuntu firewall may be on: `sudo ufw allow 9000/tcp` |
| No IP address at all | The wrong host network card is selected in the bridged adapter settings. |
| Works from the VM but not from Windows on Wi-Fi | Some Wi-Fi networks (public, hotel, campus) block device-to-device traffic. Try Ethernet or a home network. |

Quick check from Windows PowerShell:

```powershell
Test-NetConnection <VM-IP> -Port 9000
```
