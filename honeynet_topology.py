#!/usr/bin/python
# honeynet_topology.py

from mininet.net import Mininet
from mininet.node import Host, Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import os

def runHoneynet():
    "Creates a simple, isolated honeypot network."

    # Clean up state files from previous runs
    os.system("rm -f coordination.log")
    
    # We no longer automatically clear attack.log
    # To clear it manually, run: truncate -s 0 logs/attack.log

    net = Mininet(host=Host, waitConnected=True)

    info('*** Adding controller\n')
    net.addController('c0')

    info('*** Adding hosts\n')
    h_attacker = net.addHost('h1', ip='10.0.0.1/24')
    h_plug = net.addHost('h2', ip='10.0.0.2/24')
    h_camera = net.addHost('h3', ip='10.0.0.3/24')

    info('*** Adding switch\n')
    s1 = net.addSwitch('s1')

    info('*** Creating links\n')
    net.addLink(h_attacker, s1)
    net.addLink(h_plug, s1)
    net.addLink(h_camera, s1)

    info('*** Starting network\n')
    net.start()
    
    info('*** Starting Honeypot Services...\n')
    
    plug_cmd = ('python3 honeypot_server.py --type plug --ip 10.0.0.2 --port 1337 --id plug_1 &')
    h_plug.cmd(plug_cmd)
    
    camera_cmd = ('python3 honeypot_server.py --type camera --ip 10.0.0.3 --port 8080 --id cam_1 --linked-plug plug_1 &')
    h_camera.cmd(camera_cmd)

    info('\n*** Network is running. Instructions:\n')
    info('1. In a NEW terminal, run the alerter and/or visualizer.\n')
    info('2. Run the attack from this CLI: "h1 python3 attacker.py"\n')

    CLI(net)

    info('*** Stopping network\n')
    net.stop()
    os.system("sudo mn -c")

if __name__ == '__main__':
    setLogLevel('info')
    runHoneynet()