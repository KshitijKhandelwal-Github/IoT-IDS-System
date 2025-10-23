# honeypot_server.py
import socket
import argparse
import time
import datetime
import os

COORDINATION_FILE = 'coordination.log'
LOG_FILE = 'logs/attack.log'

def get_state(key):
    if not os.path.exists(COORDINATION_FILE): return None
    with open(COORDINATION_FILE, 'r') as f:
        for line in f:
            if line.startswith(key): return line.strip().split(':')[1]
    return None

def set_state(key, value):
    lines, found = [], False
    if os.path.exists(COORDINATION_FILE):
        with open(COORDINATION_FILE, 'r') as f: lines = f.readlines()
    with open(COORDINATION_FILE, 'w') as f:
        for i, line in enumerate(lines):
            if line.startswith(key):
                lines[i] = f"{key}:{value}\n"; found = True
        if not found: lines.append(f"{key}:{value}\n")
        f.writelines(lines)

def log_attack(attacker_ip, device_type, port, message):
    """Logs the attack details to a file for the alerter to read."""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = (
        f"Timestamp: {timestamp}\n"
        f"Device: {device_type} (Port {port})\n"
        f"Attacker IP: {attacker_ip}\n"
        f"Details: {message}\n"
    )
    with open(LOG_FILE, 'a') as f:
        f.write(log_entry + '---\n')
        f.flush() # Force write to disk
    print(f"Logged attack from {attacker_ip} on {device_type}")

def run_smart_plug(ip, port, device_id):
    set_state(f"{device_id}_power", "ON")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(1)
    print(f"🔌 Smart Plug Honeypot '{device_id}' listening on {ip}:{port}")
    while True:
        conn, addr = server_socket.accept()
        try:
            data = conn.recv(1024).decode().strip()
            log_attack(addr[0], 'Smart Plug', port, f"Received command: '{data}'")
            if data == 'off':
                set_state(f"{device_id}_power", "OFF")
                conn.sendall(b'Plug is now OFF.\n')
        finally:
            conn.close()

def run_camera(ip, port, device_id, linked_plug_id):
    print(f"📷 Smart Camera Honeypot '{device_id}' is starting up...")
    server_socket = None
    while True:
        power_state = get_state(f"{linked_plug_id}_power")
        if power_state == "ON" and server_socket is None:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((ip, port)); server_socket.listen(1); server_socket.settimeout(1.0) 
            print(f"📷 STATE: Camera '{device_id}' is ON on {ip}:{port}.")
        elif power_state == "OFF" and server_socket is not None:
            server_socket.close(); server_socket = None
            print(f"📷 STATE: Camera '{device_id}' is OFF.")
        if server_socket:
            try:
                conn, addr = server_socket.accept()
                log_attack(addr[0], 'Smart Camera', port, "Connection established.")
                conn.sendall(b'--FAKE MJPEG STREAM--\n')
                conn.close()
            except socket.timeout:
                continue
        else:
            time.sleep(2)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', required=True, choices=['plug', 'camera'])
    parser.add_argument('--ip', required=True)
    parser.add_argument('--port', type=int, required=True)
    parser.add_argument('--id', required=True)
    parser.add_argument('--linked-plug')
    args = parser.parse_args()
    os.makedirs('logs', exist_ok=True)
    if args.type == 'plug':
        run_smart_plug(args.ip, args.port, args.id)
    elif args.type == 'camera':
        run_camera(args.ip, args.port, args.id, args.linked_plug)