# CN-Orange-Problem
# SDN-Based Path Tracing Tool

## 📌 Problem Statement

The objective of this project is to design and implement a Software Defined Networking (SDN) based system that can trace the path of packets in a network and apply flow-based filtering using a centralized controller.

---

## 🎯 Objectives

* To simulate a network using Mininet
* To implement an SDN controller using POX
* To trace packet flow across switches
* To apply filtering/blocking using flow rules

---

## 🛠️ Tools & Technologies Used

* **Mininet** (Network Emulator)
* **POX Controller** (SDN Controller)
* **Python**
* **Ubuntu Linux**

---

## ⚙️ Setup & Execution Steps

### 1. Start the POX Controller

```bash
cd ~/pox
./pox.py log.level --DEBUG path_tracer
```

### 2. Start Mininet

```bash
sudo mn --controller=remote,ip=127.0.0.1,port=6633
```

---

## 🧪 Test Scenarios

### ✅ Scenario 1: Normal Communication

**Command:**

```bash
pingall
```

**Expected Result:**

* All hosts communicate successfully
* 0% packet loss
* Controller logs show packet flow

---

### 🔴 Scenario 2: Blocking Traffic

**Command:**

```bash
h1 ping h2
```

**Expected Result:**

* Ping fails or is blocked
* Controller displays:

```
Blocking traffic to 10.0.0.2
```

---

## 🔍 Working Explanation

* The controller listens for `PacketIn` events from switches
* It logs packet flow (source → destination)
* When a packet destined for a specific IP (10.0.0.2) is detected,
  the controller installs a flow rule to block further traffic
* This demonstrates SDN-based control and dynamic rule installation

---

## 📊 Expected Output

* Packet logs displayed in controller
* Successful communication in normal scenario
* Blocked traffic in filtering scenario
* Flow rules applied dynamically
---

## Extended Topology (Multi-Switch, Multi-Host)

To demonstrate scalability, a custom topology with two switches and four hosts was implemented.

### Topology Diagram

h1    h2        h3    h4
 |     |         |     |
 s1 ----------- s2

### Description

- Two switches: s1 and s2  
- Four hosts: h1, h2 connected to s1 and h3, h4 connected to s2  
- Switches are interconnected (s1 ↔ s2)  
- Enables multi-hop communication across switches  

### How to Run

1. Start the controller:
```bash
cd ~/pox
./pox.py log.level --DEBUG path_tracer
```
2. Run the custom topology
   sudo mn --custom ~/mytopo.py --topo mytopo --controller=remote,ip=127.0.0.1,port=6633
Testing
Test connectivity:
pingall
Test cross-switch communication:
h1 ping h4

Blocking Scenario

1../pox.py log.level --DEBUG path_tracer_block
2.h1 ping h2   # Blocked
h1 ping h4   # Allowed

##📸 Proof of Execution

### Controller Running
<img width="1079" height="514" alt="image" src="https://github.com/user-attachments/assets/8406967d-f52b-4354-aaa4-4b1b7e62ed09" />

### Normal Communication (pingall)

<img width="1091" height="506" alt="image" src="https://github.com/user-attachments/assets/68bdc4e3-566a-4191-9fb7-6cc1c82115c5" />


### Blocking Scenario
<img width="1086" height="505" alt="image" src="https://github.com/user-attachments/assets/fa42ef33-bdb2-4f4d-87a4-8a3262e5e5cf" />


### Path Tracing Logs

<img width="1072" height="507" alt="image" src="https://github.com/user-attachments/assets/257e4ddb-18a5-4107-9b1d-8a6b5f1dbeb5" />

##  Performance Analysis
### Throughput Measurement (iperf)

Command:
h2 iperf -s &
h1 iperf -c 10.0.0.2

Result:
~2.40 Mbits/sec

Observation:
The throughput represents the data transfer rate between hosts under SDN controller management. It depends on flow rules and network configuration.
<img width="816" height="585" alt="image" src="https://github.com/user-attachments/assets/93c4887a-0788-4fb5-aa15-981dc4d567d5" />


---

## 📚 References

* https://mininet.org
* https://github.com/noxrepo/pox
* SDN/OpenFlow documentation

---

## 👩‍💻 Author

**Namitha N Reddy**
