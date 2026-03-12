import tkinter as tk
import math
import random
import heapq

# --- SYSTEM THEME & CONFIGURATION ---
CITY_THEME = {
    "BG_DARK": "#05050a",
    "HUB_OK": "#00ffcc",
    "HUB_FAIL": "#ff0033",
    "HUB_JAMMED": "#bd00ff",
    "STORM_FLASH": "#331a00",
    "CYBER_FLASH": "#1a0033",
    "STORM_BTN": "#ff8800",
    "CYBER_BTN": "#ffffff",
    "CYBER_TEXT": "#000000",
    "REBOOT_BTN": "#39ff14",
    "CABLE_LIVE": "#00f2ff",
    "CABLE_IDLE": "#1a1c2c",
    "CABLE_JAMMED": "#4b0082",
    "TEXT_INFO": "#00ffcc",
    "SCANLINE": "#0a0a15",
    "HUD_BORDER": "#1e293b"
}

SECTORS = {
    0: {"name": "ARMY AREA", "color": "#33FF57"},
    1: {"name": "CITY CENTER", "color": "#FF33A8"},
    2: {"name": "TECH HUB", "color": "#3383FF"},
    3: {"name": "RESIDENTIAL", "color": "#FF8C33"},
    4: {"name": "IND. ZONE", "color": "#FFF333"}
}

INDIA_CITIES = [
    "New Delhi", "Mumbai", "Bangalore", "Hyderabad", "Ahmedabad",
    "Chennai", "Kolkata", "Surat", "Pune", "Jaipur", "Lucknow",
    "Kanpur", "Nagpur", "Indore", "Thane", "Bhopal", "Visakhapatnam",
    "Patna", "Vadodara", "Ghaziabad", "Ludhiana", "Agra", "Nashik"
]


class NetworkNode:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.active = True
        self.cluster_id = 0
        self.jammed = False
        self.ip = f"192.168.{random.randint(10, 99)}.{random.randint(2, 254)}"
        self.city = random.choice(INDIA_CITIES)
        self.lat = round(random.uniform(8.4, 37.6), 4)
        self.lon = round(random.uniform(68.1, 97.4), 4)
        self.signal = random.randint(45, 99)

    @property
    def sector_info(self):
        return SECTORS.get(self.cluster_id, {"name": "UNKNOWN", "color": "#fff"})


class WirelessMeshSim:
    def __init__(self, root):
        self.root = root
        self.root.title("Disaster Resilient Wireless Mesh Network | India Operations")
        self.root.geometry("1400x950")
        self.root.configure(bg=CITY_THEME["BG_DARK"])

        self.nodes = []
        self.current_path = []
        self.packets = []
        self.selected_node = None
        self.mbps = 0.0
        self.storm_active = False
        self.cyber_active = False
        self.scanline_y = 0

        self.setup_gui()
        self.reboot_system()
        self.run_engine()

    def setup_gui(self):
        header = tk.Frame(self.root, bg="#0d1117", pady=10, highlightbackground=CITY_THEME["HUD_BORDER"],
                          highlightthickness=1)
        header.pack(fill=tk.X)
        tk.Label(header, text="📡 DISASTER RESILIENT WIRELESS MESH NETWORK",
                 font=("OCR A Extended", 20, "bold"), fg=CITY_THEME["CABLE_LIVE"], bg="#0d1117").pack()

        self.canvas = tk.Canvas(self.root, bg=CITY_THEME["BG_DARK"], highlightthickness=0, cursor="target")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Binding Left Click for both Selection and Blocking
        self.canvas.bind("<Button-1>", self.on_select_and_toggle)
        self.canvas.bind("<Button-3>", self.on_select_and_toggle)

        dash = tk.Frame(self.root, bg="#080c1d", width=380, highlightbackground=CITY_THEME["HUD_BORDER"],
                        highlightthickness=1)
        dash.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 20), pady=20)
        dash.pack_propagate(False)

        tk.Label(dash, text="NETWORK THROUGHPUT", font=("Arial", 9, "bold"), fg="#475569", bg="#080c1d").pack(
            pady=(20, 0))
        self.speed_label = tk.Label(dash, text="000", font=("Consolas", 55, "bold"), fg=CITY_THEME["CABLE_LIVE"],
                                    bg="#080c1d")
        self.speed_label.pack()

        self.status_box = tk.Label(dash, text="SYSTEM NOMINAL", font=("Arial", 12, "bold"), bg=CITY_THEME["HUB_OK"],
                                   fg="black", width=28, pady=8)
        self.status_box.pack(pady=20)

        info_frame = tk.LabelFrame(dash, text="NODE TELEMETRY", bg="#080c1d", fg=CITY_THEME["CABLE_LIVE"],
                                   font=("Consolas", 10, "bold"), padx=15, pady=15)
        info_frame.pack(fill=tk.X, padx=15, pady=10)

        self.lbl_node_id = tk.Label(info_frame, text="ID: N/A", bg="#080c1d", fg="white", font=("Consolas", 11))
        self.lbl_node_id.pack(anchor="w")
        self.lbl_node_ip = tk.Label(info_frame, text="IP: --.--.--.--", bg="#080c1d", fg="#888", font=("Consolas", 10))
        self.lbl_node_ip.pack(anchor="w")

        tk.Frame(info_frame, height=1, bg="#333").pack(fill=tk.X, pady=8)

        self.lbl_node_city = tk.Label(info_frame, text="CITY: SCANNING...", bg="#080c1d", fg=CITY_THEME["HUB_OK"],
                                      font=("Consolas", 11, "bold"))
        self.lbl_node_city.pack(anchor="w")
        self.lbl_node_geo = tk.Label(info_frame, text="LAT/LON: --.----, --.----", bg="#080c1d", fg="#888",
                                     font=("Consolas", 9))
        self.lbl_node_geo.pack(anchor="w")
        self.lbl_node_sector = tk.Label(info_frame, text="SEC: UNKNOWN", bg="#080c1d", fg="white", font=("Consolas", 9))
        self.lbl_node_sector.pack(anchor="w", pady=(5, 0))

        tk.Label(info_frame, text="SIGNAL INTEGRITY:", bg="#080c1d", fg="#555", font=("Arial", 7, "bold")).pack(
            anchor="w", pady=(10, 0))
        self.signal_canvas = tk.Canvas(info_frame, height=6, bg="#111", highlightthickness=0)
        self.signal_canvas.pack(fill=tk.X, pady=2)
        self.signal_bar = self.signal_canvas.create_rectangle(0, 0, 0, 6, fill=CITY_THEME["HUB_OK"], width=0)

        btn_frame = tk.Frame(dash, bg="#080c1d")
        btn_frame.pack(fill=tk.X, padx=15, pady=20)

        tk.Button(btn_frame, text="🔄 REBOOT NETWORK", command=self.reboot_system, bg=CITY_THEME["REBOOT_BTN"],
                  fg="black", font=("Arial", 10, "bold"), relief="flat", pady=8).pack(fill=tk.X, pady=5)
        tk.Button(btn_frame, text="⚠️ TRIGGER STORM", command=self.trigger_storm, bg=CITY_THEME["STORM_BTN"],
                  fg="black", font=("Arial", 10, "bold"), relief="flat", pady=8).pack(fill=tk.X, pady=5)
        tk.Button(btn_frame, text="🛡️ CYBER INTRUSION (ARMY)", command=self.toggle_cyber, bg=CITY_THEME["CYBER_BTN"],
                  fg=CITY_THEME["CYBER_TEXT"], font=("Arial", 10, "bold"), relief="flat", pady=8).pack(fill=tk.X,
                                                                                                       pady=5)

        self.log = tk.Text(dash, height=12, width=35, bg="#000", fg=CITY_THEME["HUB_OK"], font=("Consolas", 9), bd=0)
        self.log.pack(padx=15, pady=(0, 20), fill=tk.BOTH, expand=True)

    def log_event(self, msg):
        self.log.insert(tk.END, f"> {msg}\n")
        self.log.see(tk.END)

    def reboot_system(self):
        self.nodes, self.packets = [], []
        self.cyber_active = False
        for i in range(45):
            x, y = (60, 350) if i == 0 else (800, 350) if i == 44 else (random.randint(100, 750),
                                                                        random.randint(50, 650))
            self.nodes.append(NetworkNode(i, x, y))
        self.apply_kmeans()
        self.calculate_dijkstra()

    def apply_kmeans(self):
        centroids = [(random.randint(100, 700), random.randint(100, 600)) for _ in range(5)]
        for _ in range(5):
            for n in self.nodes:
                dists = [math.hypot(n.x - c[0], n.y - c[1]) for c in centroids]
                n.cluster_id = dists.index(min(dists))
            new_centroids = [[0, 0, 0] for _ in range(5)]
            for n in self.nodes:
                new_centroids[n.cluster_id][0] += n.x
                new_centroids[n.cluster_id][1] += n.y
                new_centroids[n.cluster_id][2] += 1
            centroids = [
                (c[0] / c[2], c[1] / c[2]) if c[2] > 0 else (random.randint(100, 700), random.randint(100, 600)) for c
                in new_centroids]

    def on_select_and_toggle(self, event):
        target_node = None
        for n in self.nodes:
            if math.hypot(event.x - n.x, event.y - n.y) < 25:
                target_node = n
                break

        if target_node:
            # 1. Block/Unblock logic
            target_node.active = not target_node.active

            # 2. Update Sidebar Info
            self.selected_node = target_node
            self.lbl_node_id.config(text=f"ID: NODE-{target_node.id:02d}")
            self.lbl_node_ip.config(text=f"IP: {target_node.ip}")
            self.lbl_node_city.config(text=f"📍 {target_node.city.upper()}")
            self.lbl_node_geo.config(text=f"LAT: {target_node.lat} N  LON: {target_node.lon} E")
            sector = target_node.sector_info
            self.lbl_node_sector.config(text=f"SEC: {sector['name']}", fg=sector["color"])

            # Update Signal Bar
            w = self.signal_canvas.winfo_width()
            self.signal_canvas.coords(self.signal_bar, 0, 0, w * (target_node.signal / 100), 6)

            # 3. Recalculate and Log
            self.calculate_dijkstra()
            status = "BLOCKED" if not target_node.active else "ACTIVE"
            self.log_event(f"NODE {target_node.id} SET TO {status}")

    def toggle_cyber(self):
        self.cyber_active = not self.cyber_active
        for n in self.nodes:
            n.jammed = self.cyber_active if n.sector_info["name"] == "ARMY AREA" else False
        self.calculate_dijkstra()

    def calculate_dijkstra(self):
        pq, distances, previous = [(0, 0)], {n.id: float('inf') for n in self.nodes}, {}
        distances[0] = 0
        while pq:
            curr_dist, curr_id = heapq.heappop(pq)
            if curr_id == 44: break
            u = self.nodes[curr_id]
            if not u.active or u.jammed: continue
            for v in self.nodes:
                if v.id != u.id and v.active and not v.jammed:
                    dist = math.hypot(u.x - v.x, u.y - v.y)
                    if dist < 160:
                        new_dist = curr_dist + dist
                        if new_dist < distances[v.id]:
                            distances[v.id], previous[v.id] = new_dist, u.id
                            heapq.heappush(pq, (new_dist, v.id))
        path, curr = [], 44
        while curr in previous:
            path.append(curr)
            curr = previous[curr]
        self.current_path = [0] + path[::-1] if path else []

        # Update Status Box
        if not self.current_path:
            self.status_box.config(text="LINK SEVERED", bg=CITY_THEME["HUB_FAIL"], fg="white")
        elif self.cyber_active:
            self.status_box.config(text="ARMY SECTOR JAMMED", bg=CITY_THEME["HUB_JAMMED"], fg="white")
        else:
            self.status_box.config(text="SYSTEM NOMINAL", bg=CITY_THEME["HUB_OK"], fg="black")

    def trigger_storm(self):
        self.storm_active = True
        targets = random.sample([n for n in self.nodes if n.id not in [0, 44] and n.active], 8)
        for n in targets: n.active = False
        self.calculate_dijkstra()
        self.root.after(1200, lambda: setattr(self, 'storm_active', False))

    def run_engine(self):
        self.canvas.delete("all")
        self.canvas.config(bg=CITY_THEME["STORM_FLASH"] if self.storm_active else CITY_THEME["BG_DARK"])

        # Scanline
        h = self.canvas.winfo_height()
        self.scanline_y = (self.scanline_y + 3) % h
        self.canvas.create_line(0, self.scanline_y, 1000, self.scanline_y, fill=CITY_THEME["SCANLINE"], width=1)

        # Draw Cables
        for n1 in self.nodes:
            if not n1.active: continue
            for n2 in self.nodes:
                if n1.id < n2.id and n2.active and math.hypot(n1.x - n2.x, n1.y - n2.y) < 160:
                    is_path = self.current_path and any(
                        {n1.id, n2.id} == {self.current_path[k], self.current_path[k + 1]} for k in
                        range(len(self.current_path) - 1))
                    color = CITY_THEME["CABLE_JAMMED"] if n1.jammed or n2.jammed else CITY_THEME[
                        "CABLE_LIVE"] if is_path else CITY_THEME["CABLE_IDLE"]
                    self.canvas.create_line(n1.x, n1.y, n2.x, n2.y, fill=color, width=3 if is_path else 1)

        # Draw Nodes
        for n in self.nodes:
            outline = CITY_THEME["HUB_FAIL"] if not n.active else CITY_THEME["HUB_JAMMED"] if n.jammed else \
            n.sector_info["color"]
            if n.id == 0: outline = "#fff"
            if n.id == 44: outline = "#d400ff"

            if self.selected_node and n.id == self.selected_node.id:
                self.canvas.create_oval(n.x - 15, n.y - 15, n.x + 15, n.y + 15, outline="white", dash=(2, 2))

            self.canvas.create_rectangle(n.x - 8, n.y - 8, n.x + 8, n.y + 8, outline=outline, width=2, fill="#000")
            if n.active: self.canvas.create_oval(n.x - 3, n.y - 3, n.x + 3, n.y + 3, fill=outline)
            self.canvas.create_text(n.x, n.y - 15, text=str(n.id), fill="white", font=("Arial", 8, "bold"))

        # Packets & Throughput
        if self.current_path and not self.nodes[0].jammed:
            self.mbps = random.uniform(10, 200)
            if random.random() < 0.3: self.packets.append({"idx": 0, "prog": 0})
        else:
            self.mbps = 0.0
        self.speed_label.config(text=f"{self.mbps:.0f}")

        new_packets = []
        for p in self.packets:
            if p["idx"] < len(self.current_path) - 1:
                u, v = self.nodes[self.current_path[p["idx"]]], self.nodes[self.current_path[p["idx"] + 1]]
                p["prog"] += 0.2
                if p["prog"] >= 1: p["prog"], p["idx"] = 0, p["idx"] + 1
                px, py = u.x + (v.x - u.x) * p["prog"], u.y + (v.y - u.y) * p["prog"]
                self.canvas.create_oval(px - 3, py - 3, px + 3, py + 3, fill="#fff")
                new_packets.append(p)
        self.packets = new_packets
        self.root.after(50, self.run_engine)


if __name__ == "__main__":
    root = tk.Tk()
    sim = WirelessMeshSim(root)
    root.mainloop()
