# SDN Learning Switch Controller

## Overview

This project implements a Learning Switch Controller using Software Defined Networking (SDN) principles. The controller is developed using the POX platform and interacts with a network emulated in Mininet.
The controller mimics the behavior of a traditional Ethernet learning switch by dynamically learning MAC addresses and installing flow rules in the switch.

## Objectives
Implement a custom SDN controller (no built-in modules)
Learn MAC-to-port mappings dynamically
Reduce unnecessary flooding
Install flow rules for efficient packet forwarding

## Architecture Diagram
        +---------------------+
        |    POX Controller   |
        | (Learning Switch)   |
        +----------+----------+
                   |
            OpenFlow Protocol
                   |
        +----------+----------+
        |       Switch (s1)   |
        |   Open vSwitch      |
        +----+----------+-----+
             |          |
           h1          h2

## Workflow

1. Mininet hosts send packets
2. OpenFlow switch forwards unknown packets to controller (PacketIn)
3. Controller processes packet:
   - Learns source MAC → port
   - Checks destination MAC
4. If known:
   - Installs flow rule in switch
   - Packet forwarded directly
5. If unknown:
   - Packet is flooded
6. Future packets follow installed flow rules (no controller involvement)

## How It Works
When a packet arrives at the switch:
It is forwarded to the controller (PacketIn event)
The controller:
Learns the source MAC address → input port
Checks if the destination MAC is known
If destination is known:
Installs a flow rule
Sends packet directly to the correct port
If destination is unknown:
Floods the packet to all ports

## Project Structure
SDN-Learning-Switch/
│
├── my_learning_switch.py   # Custom POX controller code
├── README.md            # Project documentation

## Prerequisites
Ubuntu (VM recommended)
Python 2.7 (for POX)
Mininet
Open vSwitch

## Install dependencies:
sudo apt update
sudo apt install mininet openvswitch-switch

## How to Run
1. Start POX Controller
cd pox
./pox.py forwarding.my_learning_switch
2. Start Mininet
sudo mn --topo single,3 --controller remote --mac
3. Test Connectivity
pingall
4. View Flow Rules
sudo ovs-ofctl dump-flows s1

## Performance Analysis

We evaluated network performance using:

### 🔹 Latency (Ping)
- First ping: Higher delay due to flooding
- Subsequent pings: Lower delay due to flow rules

### 🔹 Throughput (iperf)
- Stable throughput observed
- No packet loss in small topology

### 🔹 Flow Table Behavior
- Initially empty
- Populated after first communication
- Reduces controller load

### Conclusion:
Flow rules significantly improve efficiency after initial learning phase.

## Output
<img width="804" height="186" alt="image" src="https://github.com/user-attachments/assets/e22613dd-570e-4fcb-ab7b-9c475d70b182" />
<img width="769" height="619" alt="image" src="https://github.com/user-attachments/assets/fc349727-97d4-4fcb-9896-3a61200f90e1" />
<img width="1365" height="679" alt="image" src="https://github.com/user-attachments/assets/a3cbb348-d627-43b4-8974-c78f3467e1d5" />

## Conclusion

This project demonstrates how SDN can replicate traditional switch behavior using a centralized controller. 
By dynamically learning MAC addresses and installing flow rules, the network becomes more efficient and scalable.

## Author
Yeshaswinie D
