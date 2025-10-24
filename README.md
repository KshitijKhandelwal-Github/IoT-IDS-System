# IoT Honeypot Simulation 🍯
This project creates a simulated IoT smart home environment using Mininet to act as a honeypot for detecting and analyzing cyber attacks. It features a coordinated deception mechanism, a live GUI dashboard, and a real-time, intelligent alerting system via a Telegram bot.

---

## Features ✨
**Simulated IoT Network:** Uses Mininet to create a virtual network with multiple IoT devices (a smart plug, a smart camera) and an attacker node.

**Coordinated Deception:** Honeypots are linked. Compromising one device (e.g., turning off the smart plug) causes a realistic state change in another (the camera turns off), making the simulation more believable to an attacker.

**Intelligent IDS Alerter:** A standalone script watches for attacks and sends tiered alerts to Telegram, escalating from "New Connection" to "Suspicious Scan" to "Exploit Attempt".

**Interactive Telegram Bot:** Interact with your honeynet from anywhere. Use /status to check if devices are online and /getlogs to retrieve the latest attack logs.

**Live GUI Dashboard:** An optional Tkinter-based GUI provides a real-time visual representation of the network status and live attack logs.

**Secure:** API keys and secrets are kept out of the code using a .env file.

---

## Architecture 🏗️
The project uses a "split architecture" for robustness. The Mininet simulation is completely offline. The honeypots inside Mininet only detect attacks and write to log files. Separate "alerter" and "bot" scripts run on the main machine, read these log files, and handle all internet communication.
```
+---------------------------------+      +--------------------------------+
|       Main VM (Online)          |      |    Mininet Simulation (Offline)  |
|                                 |      |                                |
|  [ Alerter ] ---> Telegram API  |      |  [ Attacker ] ---+               |
|      ^   ^                      |      |                  |               |
|      |   | Reads                |      |                  v               |
|      |   +----------------------+----->|  [ Switch ]<---->[ Honeypots ] |
|      |                          |      |      ^               |           |
|  [ Bot ] <---> Telegram API     |      |      | Writes to     |           |
|      ^                          |      |      |               v           |
|      | Reads                    |      |      +----------->[ Log Files ]  |
|      +--------------------------+      +--------------------------------+
|                                 |
+---------------------------------+
```
--- 

## Setup and Installation ⚙️

**1. Prerequisites**
Make sure you have the following installed on your Linux VM:
- Python 3.8+
- Mininet
- Git

**2. Clone the Repository**
``` bash
git clone https://github.com/YourUsername/iot-honeypot-simulation.git
cd iot-honeypot-simulation
```

**3. Install Dependencies**
Create a requirements.txt file:
``` bash
pip3 install -r requirements.txt
sudo apt-get install python3-tk
```

**4. Configure Your Secrets**
Your Telegram API keys are stored securely in a .env file.
- Create the file:
``` Bash
nano .env
```
- Add your credentials like this:
  **TELEGRAM_TOKEN**="1234567890:ABCdEfGhIjKlMnOpQrStUvWxYz"
  **CHAT_ID**="123456789"
- Save and exit.

**5. Set File Permissions**
Run this one-time command in your project directory to ensure all scripts can run and write to the log files without permission errors.
```Bash
sudo chown -R $(whoami) .
```

## How to Run the Project ▶️
You will need at least two terminals open on your Mininet VM.

**Terminal 1: Start the Bots & GUI**
In this terminal, you'll start the services that run on the main VM.

- Start the Intelligent Alerter:

``` Bash
python3 telegram_alerter.py
```
- (Optional) In another new terminal, start the Command Bot:
``` Bash
python3 command_bot.py
```
- (Optional) In another new terminal, start the GUI:
``` Bash
python3 visualizer.py
```
**Terminal 2: Start the Simulation**
This is where you'll run Mininet.
Start the simulation (this requires sudo):
``` Bash
sudo python3 honeynet_topology.py
```
Once you see the mininet> prompt, run the simulated attack:
```
mininet> h1 python3 attacker.py
```
Watch your Telegram and the GUI to see the alerts and status changes in real-time!
