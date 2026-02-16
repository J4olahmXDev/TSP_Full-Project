import tkinter as tk
from tkinter import ttk, messagebox
import calculation_module as calc

class AppUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Logistics Route Planner")
        self.root.geometry("1100x750")
        
        # --- COLOR PALETTE (Enterprise Harmony) ---
        # ใช้โทนน้ำเงินเข้ม-เทา (Professional Trust)
        self.colors = {
            "bg_main": "#F1F5F9",       # พื้นหลังเทาอ่อนมาก
            "bg_sidebar": "#FFFFFF",    # พื้นหลังแถบซ้ายขาวสะอาด
            "primary": "#0F172A",       # สีน้ำเงินเข้มเกือบดำ (Slate 900) - หัวข้อ/ปุ่มหลัก
            "accent": "#2563EB",        # สีน้ำเงินสด (Royal Blue) - Highlight/เส้นกราฟ
            "text_header": "#1E293B",   # สีตัวหนังสือหลัก
            "text_body": "#475569",     # สีตัวหนังสือรอง
            "border": "#E2E8F0",        # สีเส้นขอบบางๆ
            "input_bg": "#F8FAFC",      # สีพื้นช่องกรอก
            "success": "#10B981"        # สีเขียว (ใช้ตอนเสร็จ)
        }
        self.root.configure(bg=self.colors["bg_main"])

        # ตัวแปรระบบ
        self.cities = []
        self.target_cities = 0
        
        # ตั้งค่า Style
        self.setup_styles()
        # สร้างหน้าจอ
        self.create_layout()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame Styles
        style.configure("TFrame", background=self.colors["bg_main"])
        style.configure("Sidebar.TFrame", background=self.colors["bg_sidebar"])
        style.configure("Card.TFrame", background="#FFFFFF", relief="flat")
        
        # Label Styles
        style.configure("Header.TLabel", font=("Arial", 16, "bold"), background=self.colors["bg_sidebar"], foreground=self.colors["text_header"])
        style.configure("SubHeader.TLabel", font=("Arial", 10, "bold"), background=self.colors["bg_sidebar"], foreground=self.colors["text_body"])
        style.configure("Label.TLabel", font=("Arial", 10), background=self.colors["bg_sidebar"], foreground=self.colors["text_body"])
        
        # Entry Styles (Clean & Flat)
        style.configure("TEntry", fieldbackground=self.colors["input_bg"], bordercolor=self.colors["border"], insertcolor=self.colors["primary"])
        
        # Button Styles
        style.configure("Primary.TButton", font=("Arial", 10, "bold"), background=self.colors["primary"], foreground="white", borderwidth=0)
        style.map("Primary.TButton", background=[('active', '#334155')]) 
        
        style.configure("Secondary.TButton", font=("Arial", 10), background="white", foreground=self.colors["text_body"], bordercolor=self.colors["border"])
        style.map("Secondary.TButton", background=[('active', '#F1F5F9')])

        # Progress Bar
        style.configure("Horizontal.TProgressbar", background=self.colors["accent"], troughcolor=self.colors["border"], bordercolor=self.colors["border"])

        # Treeview (Table)
        style.configure("Treeview", background="white", fieldbackground="white", foreground=self.colors["text_header"], rowheight=28, font=("Arial", 10))
        style.configure("Treeview.Heading", background="#F8FAFC", foreground=self.colors["text_body"], font=("Arial", 9, "bold"))
        style.map("Treeview", background=[('selected', self.colors["primary"])], foreground=[('selected', 'white')])

    def create_layout(self):
        # Container หลัก แบ่งซ้ายขวา
        main_container = tk.Frame(self.root, bg=self.colors["bg_main"])
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # ================= LEFT SIDEBAR (Controls) =================
        sidebar = ttk.Frame(main_container, style="Sidebar.TFrame", padding=25)
        sidebar.pack(side="left", fill="y", padx=(0, 20)) # Fixed width by content
        
        # Logo / Title
        ttk.Label(sidebar, text="LOGISTICS PLANNER", style="Header.TLabel").pack(anchor="w", pady=(0, 5))
        ttk.Label(sidebar, text="Route Optimization Module", font=("Arial", 9), background=self.colors["bg_sidebar"], foreground="#94A3B8").pack(anchor="w", pady=(0, 25))

        # --- SECTION 1: Config ---
        ttk.Label(sidebar, text="CONFIGURATION", style="SubHeader.TLabel").pack(anchor="w", pady=(0, 10))
        
        cfg_frame = tk.Frame(sidebar, bg=self.colors["bg_sidebar"])
        cfg_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Label(cfg_frame, text="Total Nodes:", style="Label.TLabel").pack(side="left")
        
        # Validation Command (บังคับกรอกตัวเลข)
        vcmd = (self.root.register(self.validate_int), '%P')
        self.ent_target = ttk.Entry(cfg_frame, width=8, justify="center", validate="key", validatecommand=vcmd)
        self.ent_target.pack(side="left", padx=10)
        
        self.btn_set = ttk.Button(cfg_frame, text="Confirm", style="Primary.TButton", width=8, command=self.set_target)
        self.btn_set.pack(side="left")

        # Separator
        tk.Frame(sidebar, height=1, bg=self.colors["border"]).pack(fill="x", pady=10)

        # --- SECTION 2: Input ---
        self.lbl_step2 = ttk.Label(sidebar, text="DATA INPUT (Disabled)", style="SubHeader.TLabel", foreground="#CBD5E1")
        self.lbl_step2.pack(anchor="w", pady=(0, 15))

        # Input Fields with Validation
        vcmd_float = (self.root.register(self.validate_float), '%P')

        self.create_input_row(sidebar, "Location Name", "ent_name")
        self.create_input_row(sidebar, "Latitude (X)", "ent_x", validate=vcmd_float)
        self.create_input_row(sidebar, "Longitude (Y)", "ent_y", validate=vcmd_float)

        self.btn_add = ttk.Button(sidebar, text="Add Node", style="Primary.TButton", command=self.add_city, state="disabled")
        self.btn_add.pack(fill="x", pady=(20, 10))

        # Progress
        self.lbl_progress = ttk.Label(sidebar, text="0 / 0 Nodes Added", font=("Arial", 9), background=self.colors["bg_sidebar"], foreground=self.colors["text_body"])
        self.lbl_progress.pack(anchor="w", pady=(0, 5))
        self.progress = ttk.Progressbar(sidebar, orient="horizontal", mode="determinate")
        self.progress.pack(fill="x", pady=(0, 20))

        # Separator
        tk.Frame(sidebar, height=1, bg=self.colors["border"]).pack(fill="x", pady=10)

        # --- SECTION 3: Action ---
        self.btn_calc = ttk.Button(sidebar, text="Calculate Optimal Route", style="Primary.TButton", command=self.run_process, state="disabled")
        self.btn_calc.pack(fill="x", pady=(0, 10))
        
        ttk.Button(sidebar, text="System Reset", style="Secondary.TButton", command=self.reset).pack(fill="x")

        # ================= RIGHT CONTENT (Visuals) =================
        content = tk.Frame(main_container, bg=self.colors["bg_main"])
        content.pack(side="right", fill="both", expand=True)

        # 1. Table Panel
        tbl_frame = ttk.Frame(content, style="Card.TFrame", padding=1)
        tbl_frame.pack(fill="x", pady=(0, 15))
        
        cols = ("name", "x", "y")
        self.tree = ttk.Treeview(tbl_frame, columns=cols, show="headings", height=6)
        self.tree.heading("name", text="Location Name")
        self.tree.heading("x", text="Latitude (X)")
        self.tree.heading("y", text="Longitude (Y)")
        
        self.tree.column("name", width=150)
        self.tree.column("x", width=100, anchor="e") # e = ชิดขวาเพื่อให้ตัวเลขตรงกัน
        self.tree.column("y", width=100, anchor="e")
        
        self.tree.pack(fill="both", expand=True)

        # 2. Result Panel (Route Text)
        self.res_frame = ttk.Frame(content, style="Card.TFrame", padding=15)
        self.res_frame.pack(fill="x", pady=(0, 15))
        
        self.lbl_total_dist = tk.Label(self.res_frame, text="Total Distance: 0.0000 Units", font=("Arial", 12, "bold"), bg="white", fg=self.colors["text_header"])
        self.lbl_total_dist.pack(anchor="w")
        
        tk.Label(self.res_frame, text="Travel Sequence:", font=("Arial", 9, "bold"), bg="white", fg="#64748B").pack(anchor="w", pady=(5,0))
        self.lbl_route_text = tk.Label(self.res_frame, text="-", font=("Consolas", 10), bg="#F8FAFC", fg=self.colors["primary"], padx=10, pady=5, justify="left", wraplength=600)
        self.lbl_route_text.pack(fill="x", pady=(5,0))

        # 3. Graph Panel
        graph_frame = ttk.Frame(content, style="Card.TFrame", padding=10)
        graph_frame.pack(fill="both", expand=True)
        
        self.canvas = tk.Canvas(graph_frame, bg="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda e: self.draw_graph(None))

    # --- Helper: Create Input Row ---
    def create_input_row(self, parent, label, var_name, validate=None):
        f = tk.Frame(parent, bg=self.colors["bg_sidebar"])
        f.pack(fill="x", pady=5)
        tk.Label(f, text=label, bg=self.colors["bg_sidebar"], fg=self.colors["text_body"], font=("Arial", 9)).pack(anchor="w")
        
        entry_opts = {"width": 25}
        if validate:
            entry_opts["validate"] = "key"
            entry_opts["validatecommand"] = validate
            
        entry = ttk.Entry(f, **entry_opts)
        entry.pack(fill="x", pady=(2, 0))
        entry.config(state="disabled") # Disabled by default
        setattr(self, var_name, entry)

    # --- VALIDATION LOGIC (บังคับกรอกตัวเลข) ---
    def validate_int(self, P):
        if P == "": return True
        return P.isdigit()

    def validate_float(self, P):
        if P == "": return True
        try:
            float(P)
            return True
        except ValueError:
            return False

    # --- APP LOGIC ---
    def set_target(self):
        val = self.ent_target.get()
        if not val or int(val) < 2:
            messagebox.showwarning("System", "Please enter at least 2 nodes.")
            return
        
        self.target_cities = int(val)
        self.cities = []
        
        # Lock Config, Unlock Inputs
        self.ent_target.config(state="disabled")
        self.btn_set.config(state="disabled")
        
        self.lbl_step2.config(foreground=self.colors["text_header"], text="DATA INPUT (Active)")
        self.ent_name.config(state="normal")
        self.ent_x.config(state="normal")
        self.ent_y.config(state="normal")
        self.btn_add.config(state="normal")
        
        self.update_ui_state()
        self.ent_name.focus()

    def add_city(self):
        name = self.ent_name.get()
        x_val = self.ent_x.get()
        y_val = self.ent_y.get()

        if not name or not x_val or not y_val:
            return # Validation handled by entry constraints mostly

        x, y = float(x_val), float(y_val)
        
        self.cities.append({'name': name, 'x': x, 'y': y})
        
        # Format .4f (4 ตำแหน่ง)
        self.tree.insert("", "end", values=(name, f"{x:.4f}", f"{y:.4f}"))
        
        # Clear Inputs
        self.ent_name.delete(0, tk.END)
        self.ent_x.delete(0, tk.END)
        self.ent_y.delete(0, tk.END)
        self.ent_name.focus()
        
        self.update_ui_state()
        self.draw_graph(None) # Preview dot

    def update_ui_state(self):
        curr = len(self.cities)
        tgt = self.target_cities
        
        self.lbl_progress.config(text=f"{curr} / {tgt} Nodes Added")
        if tgt > 0:
            self.progress["value"] = (curr / tgt) * 100
        
        if curr >= tgt and tgt > 0:
            # Lock Inputs
            self.ent_name.config(state="disabled")
            self.ent_x.config(state="disabled")
            self.ent_y.config(state="disabled")
            self.btn_add.config(state="disabled")
            
            # Unlock Calculate
            self.btn_calc.config(state="normal")
            messagebox.showinfo("System", "Data entry complete. Ready to calculate.")

    def run_process(self):
        dist, path = calc.solve_tsp_nearest_neighbor(self.cities)
        
        # 1. Update Distance
        self.lbl_total_dist.config(text=f"Total Distance: {dist:.4f} Units", fg=self.colors["success"])
        
        # 2. Update Route Text (A -> B -> C -> A)
        route_str = " ➔ ".join([c['name'] for c in path])
        self.lbl_route_text.config(text=route_str)
        
        # 3. Draw Graph
        self.draw_graph(path)

    def reset(self):
        self.cities = []
        self.target_cities = 0
        
        # Reset Widgets
        for item in self.tree.get_children(): self.tree.delete(item)
        
        self.ent_target.config(state="normal"); self.ent_target.delete(0, tk.END)
        self.btn_set.config(state="normal")
        
        self.ent_name.config(state="disabled"); self.ent_name.delete(0, tk.END)
        self.ent_x.config(state="disabled"); self.ent_x.delete(0, tk.END)
        self.ent_y.config(state="disabled"); self.ent_y.delete(0, tk.END)
        self.btn_add.config(state="disabled")
        self.btn_calc.config(state="disabled")
        
        self.lbl_progress.config(text="0 / 0 Nodes Added")
        self.progress["value"] = 0
        self.lbl_total_dist.config(text="Total Distance: 0.0000 Units", fg=self.colors["text_header"])
        self.lbl_route_text.config(text="-")
        
        self.canvas.delete("all")

    def draw_graph(self, route_path):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        
        # Grid Background
        step = 50
        for i in range(0, w, step): self.canvas.create_line(i, 0, i, h, fill="#F1F5F9")
        for i in range(0, h, step): self.canvas.create_line(0, i, w, i, fill="#F1F5F9")

        if not self.cities: return

        # Scaling Logic
        xs = [c['x'] for c in self.cities]
        ys = [c['y'] for c in self.cities]
        
        # Handle case where all points are same or only 1 point
        if len(set(xs)) < 2: xs.append(xs[0]+1); xs.append(xs[0]-1)
        if len(set(ys)) < 2: ys.append(ys[0]+1); ys.append(ys[0]-1)
            
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        pad = 50
        
        def to_px(x, y):
            # Safe division
            rx = (max_x - min_x) if (max_x - min_x) != 0 else 1
            ry = (max_y - min_y) if (max_y - min_y) != 0 else 1
            
            px = pad + (x - min_x) / rx * (w - 2*pad)
            py = h - (pad + (y - min_y) / ry * (h - 2*pad)) # Flip Y
            return px, py

        # --- DRAW ROUTE WITH ARROWS (Fix: Directional Arrows) ---
        if route_path:
            for i in range(len(route_path)-1):
                c1 = route_path[i]
                c2 = route_path[i+1]
                
                x1, y1 = to_px(c1['x'], c1['y'])
                x2, y2 = to_px(c2['x'], c2['y'])
                
                # ใช้ arrow=tk.LAST เพื่อให้หัวลูกศรอยู่ปลายทางเสมอ
                self.canvas.create_line(x1, y1, x2, y2, fill=self.colors["accent"], width=2, 
                                      arrow=tk.LAST, arrowshape=(10, 12, 5), dash=(4, 2))

        # --- DRAW NODES ---
        for i, c in enumerate(self.cities):
            px, py = to_px(c['x'], c['y'])
            
            # Start node = Green, Others = Blue/Dark
            fill_col = self.colors["success"] if i == 0 else "white"
            outline_col = self.colors["success"] if i == 0 else self.colors["primary"]
            
            r = 5
            self.canvas.create_oval(px-r, py-r, px+r, py+r, fill=fill_col, outline=outline_col, width=2)
            
            # Text Label with Coordinates .4f
            label_text = f"{c['name']}\n({c['x']:.2f}, {c['y']:.2f})"
            self.canvas.create_text(px, py-20, text=label_text, font=("Arial", 8), fill=self.colors["text_body"], justify="center")