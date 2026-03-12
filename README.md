# 📡 Disaster-Resilient Wireless Mesh Network Simulator

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-blue?style=for-the-badge)
![Networking](https://img.shields.io/badge/Domain-Network_Security-red?style=for-the-badge)

A highly interactive Python-based simulator designed to model wireless mesh networks capable of maintaining connectivity, testing routing efficiency, and demonstrating reliable node failure recovery under extreme crisis conditions (natural disasters and cyber intrusions).

![Wireless Mesh Network UI](Screenshot%202026-03-12%20163806.png)

## 📌 Overview
During natural disasters or targeted cyber attacks, traditional communication infrastructure often fails. This project visualizes how a self-healing wireless mesh network dynamically reroutes data packets when nodes go offline. It features live throughput calculation, dynamic sector clustering, and interactive threat simulations.

## 🚀 Key Features
* **Dynamic Shortest-Path Routing:** Implements **Dijkstra's Algorithm** (`heapq`) to calculate and visualize the most efficient data path in real-time. If a node fails, the system instantly reroutes the connection.
* **Interactive Node Management:** Left/Right-click any node on the canvas to manually block or activate it, simulating localized hardware failures or repairs.
* **Threat & Disaster Simulation:**
  * ⚠️ **Trigger Storm:** Randomly disables 8 active nodes across the map to test disaster recovery.
  * 🛡️ **Cyber Intrusion:** Simulates a targeted jamming attack on the "Army Area" sector, forcing the network to bypass compromised nodes.
* **Live Telemetry Dashboard:** Tracks simulated network throughput (Mbps), system status, node IP addresses, geolocations across Indian cities, and signal integrity.
* **Sector Clustering:** Uses a custom implementation of **K-Means clustering** to group nodes into specific operational sectors (Army Area, City Center, Tech Hub, Residential, Industrial Zone).

## 🛠️ Tech Stack & Libraries
This project is built entirely using Python and its standard libraries—no external `pip` installations required.
* **Language:** Python 3.x
* **GUI Framework:** `tkinter`
* **Core Libraries:** `math`, `random`, `heapq` (for priority queue in Dijkstra's)

## 💻 How to Run

1. Clone the repository:
   ```bash
   git clone [https://github.com/Gautam-afk-eng/Wireless-Mesh-Network-Simulator.git](https://github.com/Gautam-afk-eng/Wireless-Mesh-Network-Simulator.git)# Wireless-Mesh-Network-Simulator
