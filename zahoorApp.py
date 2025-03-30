import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D  # For 3D plotting
import csv
import json
import numpy as np
import requests  # For internet connectivity

# Global constant and simulation steps
C = 3e8  # Speed of light (m/s)
TOTAL_STEPS = 100

# Global theme flag
DARK_MODE = False

# ==================== Tab 1: Mass-Energy Conversion ====================
class MassEnergyConversionTab:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        tk.Label(parent, text="Enter Mass (kg):", font=("Arial", 14)).pack(pady=5)
        self.entry = tk.Entry(parent, font=("Arial", 14))
        self.entry.pack(pady=5)
        self.entry.insert(0, "70")
        self.convert_btn = tk.Button(parent, text="Convert to Energy", font=("Arial", 14), command=self.convert)
        self.convert_btn.pack(pady=10)
        self.result_label = tk.Label(parent, text="Energy: ", font=("Arial", 16), fg="green")
        self.result_label.pack(pady=5)
        
        self.fig, self.ax = plt.subplots(figsize=(5, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().pack(pady=10)
        
    def convert(self):
        try:
            mass = float(self.entry.get())
            if mass <= 0:
                messagebox.showerror("Input Error", "Mass must be positive.")
                return
            energy = mass * (C ** 2)
            self.result_label.config(text=f"Energy: {energy:.2e} Joules")
            self.ax.clear()
            categories = ["Mass (kg)", "Energy (scaled)"]
            values = [mass, energy / 1e16]  # Energy scaled for visualization
            bars = self.ax.bar(categories, values, color=["blue", "red"])
            for bar in bars:
                h = bar.get_height()
                self.ax.text(bar.get_x() + bar.get_width()/2, h, f"{h:.2f}", ha='center', va='bottom')
            self.ax.set_title("Mass-Energy Conversion (E=mc²)")
            self.canvas.draw()
            self.app.update_status("Mass-Energy conversion completed.")
        except ValueError:
            messagebox.showerror("Input Error", "Enter a valid number.")

# ==================== Tab 2: Advanced Mass Conservation Tracker ====================
class AdvancedMassConservationTrackerTab:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.running = False
        self.paused = False
        self.step = 0
        self.total_steps = TOTAL_STEPS
        self.sim_data = []
        
        self.transformation_options = {"Decay": 0.9, "Burn": 0.7, "Fusion": 0.5, "Explosion": 0.2, "Nuclear Fusion": 0.3}
        
        input_frame = tk.Frame(parent)
        input_frame.pack(pady=5)
        tk.Label(input_frame, text="Transformation:", font=("Arial", 14)).grid(row=0, column=0, padx=5, pady=5)
        self.transformation_var = tk.StringVar(value="Fusion")
        self.dropdown = ttk.Combobox(input_frame, textvariable=self.transformation_var, 
                                     values=list(self.transformation_options.keys()), 
                                     state="readonly", font=("Arial", 14), width=12)
        self.dropdown.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(input_frame, text="Initial Mass (kg):", font=("Arial", 14)).grid(row=0, column=2, padx=5, pady=5)
        self.mass_entry = tk.Entry(input_frame, font=("Arial", 14), width=10)
        self.mass_entry.grid(row=0, column=3, padx=5, pady=5)
        self.mass_entry.insert(0, "70")
        
        tk.Label(input_frame, text="Reaction Rate (%):", font=("Arial", 14)).grid(row=1, column=0, padx=5, pady=5)
        self.rate_entry = tk.Entry(input_frame, font=("Arial", 14), width=10)
        self.rate_entry.grid(row=1, column=1, padx=5, pady=5)
        self.rate_entry.insert(0, "100")
        tk.Label(input_frame, text="Temperature (K):", font=("Arial", 14)).grid(row=1, column=2, padx=5, pady=5)
        self.temp_entry = tk.Entry(input_frame, font=("Arial", 14), width=10)
        self.temp_entry.grid(row=1, column=3, padx=5, pady=5)
        self.temp_entry.insert(0, "300")
        tk.Label(input_frame, text="Pressure (atm):", font=("Arial", 14)).grid(row=1, column=4, padx=5, pady=5)
        self.pressure_entry = tk.Entry(input_frame, font=("Arial", 14), width=10)
        self.pressure_entry.grid(row=1, column=5, padx=5, pady=5)
        self.pressure_entry.insert(0, "1")
        
        btn_frame = tk.Frame(parent)
        btn_frame.pack(pady=10)
        self.start_btn = tk.Button(btn_frame, text="Start Simulation", font=("Arial", 14), command=self.start_simulation)
        self.start_btn.grid(row=0, column=0, padx=5)
        self.pause_btn = tk.Button(btn_frame, text="Pause", font=("Arial", 14), command=self.pause_simulation, state="disabled")
        self.pause_btn.grid(row=0, column=1, padx=5)
        self.resume_btn = tk.Button(btn_frame, text="Resume", font=("Arial", 14), command=self.resume_simulation, state="disabled")
        self.resume_btn.grid(row=0, column=2, padx=5)
        self.reset_btn = tk.Button(btn_frame, text="Reset", font=("Arial", 14), command=self.reset_simulation, state="disabled")
        self.reset_btn.grid(row=0, column=3, padx=5)
        
        self.progress = ttk.Progressbar(parent, orient="horizontal", mode="determinate", maximum=self.total_steps, length=400)
        self.progress.pack(pady=5)
        self.result_label = tk.Label(parent, text="", font=("Arial", 16))
        self.result_label.pack(pady=5)
        
        self.fig, self.ax = plt.subplots(figsize=(5,3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().pack(pady=10)
        
    def start_simulation(self):
        try:
            self.initial_mass = float(self.mass_entry.get())
            self.base_fraction = self.transformation_options[self.transformation_var.get()]
            self.reaction_rate = float(self.rate_entry.get())
            self.temperature = float(self.temp_entry.get())
            self.pressure = float(self.pressure_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Enter valid numbers for all parameters.")
            return
        if self.initial_mass <= 0:
            messagebox.showerror("Input Error", "Initial mass must be positive.")
            return
        if self.transformation_var.get() == "Nuclear Fusion":
            self.effective_fraction = 0.3 * (self.reaction_rate / 100)
        else:
            self.effective_fraction = self.base_fraction * (self.reaction_rate / 100) * (self.temperature / 300) * (self.pressure / 1)
            if self.effective_fraction > 1:
                self.effective_fraction = 1
        self.target_mass = self.initial_mass * self.effective_fraction
        self.current_mass = self.initial_mass
        self.delta = (self.initial_mass - self.target_mass) / self.total_steps
        self.step = 0
        self.sim_data = []
        self.running = True
        self.paused = False
        self.progress['value'] = 0
        self.start_btn.config(state="disabled")
        self.pause_btn.config(state="normal")
        self.reset_btn.config(state="normal")
        self.app.update_status("Advanced Mass Tracker: Simulation started.")
        self.animate()
        
    def animate(self):
        if not self.running:
            return
        if self.paused:
            self.parent.after(100, self.animate)
            return
        if self.step <= self.total_steps:
            self.current_mass = self.initial_mass - self.delta * self.step
            if self.current_mass < self.target_mass:
                self.current_mass = self.target_mass
            converted = self.initial_mass - self.current_mass
            energy = converted * (C ** 2)
            self.sim_data.append((self.step, self.current_mass, converted, energy))
            self.ax.clear()
            categories = ["Initial", "Remaining", "Converted"]
            values = [self.initial_mass, self.current_mass, converted]
            bars = self.ax.bar(categories, values, color=["blue", "green", "red"])
            for bar in bars:
                h = bar.get_height()
                self.ax.text(bar.get_x() + bar.get_width()/2, h, f"{h:.2f}", ha='center', va='bottom')
            self.ax.set_title(f"{self.transformation_var.get()} (Step {self.step}/{self.total_steps})")
            self.canvas.draw()
            self.result_label.config(text=f"Remaining Mass: {self.current_mass:.2f} kg | Energy: {energy:.2e} J")
            self.progress['value'] = self.step
            self.step += 1
            self.app.update_status(f"Advanced Tracker: Step {self.step}/{self.total_steps}")
            self.parent.after(50, self.animate)
        else:
            self.running = False
            self.pause_btn.config(state="disabled")
            self.resume_btn.config(state="disabled")
            self.app.update_status("Advanced Tracker: Simulation completed.")
            self.parent.bell()
            
    def pause_simulation(self):
        if self.running:
            self.paused = True
            self.pause_btn.config(state="disabled")
            self.resume_btn.config(state="normal")
            self.app.update_status("Advanced Tracker: Simulation paused.")
            
    def resume_simulation(self):
        if self.running and self.paused:
            self.paused = False
            self.pause_btn.config(state="normal")
            self.resume_btn.config(state="disabled")
            self.app.update_status("Advanced Tracker: Simulation resumed.")
            
    def reset_simulation(self):
        self.running = False
        self.paused = False
        self.step = 0
        self.start_btn.config(state="normal")
        self.pause_btn.config(state="disabled")
        self.resume_btn.config(state="disabled")
        self.reset_btn.config(state="disabled")
        self.result_label.config(text="Simulation reset.")
        self.ax.clear()
        self.canvas.draw()
        self.progress['value'] = 0
        self.app.update_status("Advanced Tracker: Simulation reset.")

# ==================== Tab 3: Historical Simulation Mode ====================
class HistoricalSimulationTab:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.sim_data = []
        self.running = False
        self.step = 0
        self.total_steps = TOTAL_STEPS
        self.initial_mass = 70.0
        
        top_frame = tk.Frame(parent)
        top_frame.pack(pady=5)
        tk.Label(top_frame, text="Historical Simulation Mode", font=("Arial", 16, "bold")).pack()
        
        mass_frame = tk.Frame(parent)
        mass_frame.pack(pady=5)
        tk.Label(mass_frame, text="Initial Mass (kg):", font=("Arial", 14)).grid(row=0, column=0, padx=5)
        self.mass_entry = tk.Entry(mass_frame, font=("Arial", 14), width=10)
        self.mass_entry.grid(row=0, column=1, padx=5)
        self.mass_entry.insert(0, "70")
        tk.Label(mass_frame, text="Transformation:", font=("Arial", 14)).grid(row=0, column=2, padx=5)
        self.transformation_var = tk.StringVar(value="Fusion")
        options = {"Decay": 0.9, "Burn": 0.7, "Fusion": 0.5, "Explosion": 0.2}
        self.transformation_options = options
        self.dropdown = ttk.Combobox(mass_frame, textvariable=self.transformation_var, 
                                     values=list(options.keys()), state="readonly", font=("Arial", 14), width=10)
        self.dropdown.grid(row=0, column=3, padx=5)
        
        btn_frame = tk.Frame(parent)
        btn_frame.pack(pady=10)
        self.start_btn = tk.Button(btn_frame, text="Start Historical Simulation", font=("Arial", 14), command=self.start_simulation)
        self.start_btn.grid(row=0, column=0, padx=5)
        self.stop_btn = tk.Button(btn_frame, text="Stop", font=("Arial", 14), command=self.stop_simulation, state="disabled")
        self.stop_btn.grid(row=0, column=1, padx=5)
        
        self.result_label = tk.Label(parent, text="", font=("Arial", 14))
        self.result_label.pack(pady=5)
        
        self.fig, self.ax = plt.subplots(figsize=(6,4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().pack(pady=10)
        
    def start_simulation(self):
        try:
            self.initial_mass = float(self.mass_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Enter valid mass.")
            return
        transformation = self.transformation_var.get()
        self.target_fraction = self.transformation_options[transformation]
        self.target_mass = self.initial_mass * self.target_fraction
        self.delta = (self.initial_mass - self.target_mass) / self.total_steps
        self.step = 0
        self.sim_data = []
        self.running = True
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.app.update_status("Historical Simulation: Started.")
        self.animate()
        
    def animate(self):
        if not self.running:
            return
        if self.step <= self.total_steps:
            current_mass = self.initial_mass - self.delta * self.step
            if current_mass < self.target_mass:
                current_mass = self.target_mass
            converted = self.initial_mass - current_mass
            energy = converted * (C ** 2)
            self.sim_data.append((self.step, current_mass, converted, energy))
            self.ax.clear()
            steps = [d[0] for d in self.sim_data]
            remaining = [d[1] for d in self.sim_data]
            self.ax.plot(steps, remaining, marker='o', color='green')
            self.ax.set_title("Historical Simulation: Remaining Mass Over Time")
            self.ax.set_xlabel("Step")
            self.ax.set_ylabel("Remaining Mass (kg)")
            self.canvas.draw()
            self.result_label.config(text=f"Step {self.step}: Remaining Mass = {current_mass:.2f} kg")
            self.step += 1
            self.app.update_status(f"Historical Simulation: Step {self.step}/{self.total_steps}")
            self.parent.after(100, self.animate)
        else:
            self.running = False
            self.start_btn.config(state="normal")
            self.stop_btn.config(state="disabled")
            self.app.update_status("Historical Simulation: Completed.")
            self.parent.bell()
            
    def stop_simulation(self):
        self.running = False
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.app.update_status("Historical Simulation: Stopped.")

# ==================== Tab 4: Data Logging ====================
class DataLoggingTab:
    def __init__(self, parent, data_getter, app):
        self.parent = parent
        self.data_getter = data_getter
        self.app = app
        tk.Label(parent, text="Data Logging", font=("Arial", 16, "bold")).pack(pady=10)
        
        self.tree = ttk.Treeview(parent, columns=("Step", "Remaining Mass", "Converted Mass", "Energy"), show="headings")
        self.tree.heading("Step", text="Step")
        self.tree.heading("Remaining Mass", text="Remaining Mass (kg)")
        self.tree.heading("Converted Mass", text="Converted Mass (kg)")
        self.tree.heading("Energy", text="Energy (Joules)")
        self.tree.column("Step", width=50)
        self.tree.column("Remaining Mass", width=150)
        self.tree.column("Converted Mass", width=150)
        self.tree.column("Energy", width=200)
        self.tree.pack(pady=10, fill='both', expand=True)
        
        btn_frame = tk.Frame(parent)
        btn_frame.pack(pady=10)
        self.refresh_btn = tk.Button(btn_frame, text="Refresh Data", font=("Arial", 14), command=self.populate_data)
        self.refresh_btn.grid(row=0, column=0, padx=5)
        self.export_csv_btn = tk.Button(btn_frame, text="Export CSV", font=("Arial", 14), command=self.export_csv)
        self.export_csv_btn.grid(row=0, column=1, padx=5)
        self.export_json_btn = tk.Button(btn_frame, text="Export JSON", font=("Arial", 14), command=self.export_json)
        self.export_json_btn.grid(row=0, column=2, padx=5)
        
    def populate_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        data = self.data_getter()
        if data:
            for row in data:
                self.tree.insert("", "end", values=(row[0], f"{row[1]:.2f}", f"{row[2]:.2f}", f"{row[3]:.2e}"))
            self.app.update_status("Data Logging: Data refreshed.")
        else:
            messagebox.showinfo("Data Logging", "No simulation data available. Run Historical Simulation first.")
            
    def export_csv(self):
        data = self.data_getter()
        if not data:
            messagebox.showinfo("Export", "No data available to export.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv")],
                                                 title="Save Simulation Data")
        if file_path:
            try:
                with open(file_path, mode="w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(["Step", "Remaining Mass (kg)", "Converted Mass (kg)", "Energy (Joules)"])
                    for row in data:
                        writer.writerow(row)
                messagebox.showinfo("Export", f"Data exported to {file_path}")
                self.app.update_status("Data Logging: CSV exported successfully.")
            except Exception as e:
                messagebox.showerror("Export Error", str(e))
                
    def export_json(self):
        data = self.data_getter()
        if not data:
            messagebox.showinfo("Export", "No data available to export.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                 filetypes=[("JSON files", "*.json")],
                                                 title="Save Simulation Data")
        if file_path:
            try:
                json_data = [{"Step": row[0], "Remaining Mass": row[1], "Converted Mass": row[2], "Energy": row[3]} for row in data]
                with open(file_path, mode="w") as file:
                    json.dump(json_data, file, indent=4)
                messagebox.showinfo("Export", f"Data exported to {file_path}")
                self.app.update_status("Data Logging: JSON exported successfully.")
            except Exception as e:
                messagebox.showerror("Export Error", str(e))

# ==================== Tab 5: 3D Visualization ====================
class Visualization3DTab:
    def __init__(self, parent, data_getter, app):
        self.parent = parent
        self.data_getter = data_getter
        self.app = app
        tk.Label(parent, text="3D Visualization", font=("Arial", 16, "bold")).pack(pady=10)
        self.refresh_btn = tk.Button(parent, text="Refresh 3D Plot", font=("Arial", 14), command=self.update_plot)
        self.refresh_btn.pack(pady=5)
        
        self.fig = plt.Figure(figsize=(6,5), dpi=100)
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().pack(pady=10)
        
    def update_plot(self):
        data = self.data_getter()
        if not data:
            messagebox.showinfo("3D Visualization", "No historical data available. Run Historical Simulation first.")
            return
        self.ax.clear()
        steps = [d[0] for d in data]
        remaining = [d[1] for d in data]
        energy = [d[3] for d in data]
        energy_scaled = np.array(energy) / 1e16  # Scale energy for display
        self.ax.scatter(steps, remaining, energy_scaled, c='purple', marker='o')
        self.ax.set_title("3D Scatter: Step vs Remaining Mass vs Energy")
        self.ax.set_xlabel("Step")
        self.ax.set_ylabel("Remaining Mass (kg)")
        self.ax.set_zlabel("Energy (scaled)")
        self.canvas.draw()
        self.app.update_status("3D Visualization: Plot refreshed.")

# ==================== Tab 6: Network Simulation ====================
class NetworkSimulationTab:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        tk.Label(parent, text="Multi-user Network Simulation & Internet Integration", 
                 font=("Arial", 16, "bold")).pack(pady=20)
        
        self.connect_btn = tk.Button(parent, text="Check Internet Connection", font=("Arial", 14), command=self.check_connection)
        self.connect_btn.pack(pady=10)
        
        self.send_data_btn = tk.Button(parent, text="Send Simulation Data", font=("Arial", 14), command=self.send_data)
        self.send_data_btn.pack(pady=10)
        
        self.response_text = tk.Text(parent, height=10, font=("Arial", 12))
        self.response_text.pack(pady=10, padx=10, fill="both", expand=True)
        
    def check_connection(self):
        try:
            response = requests.get("https://httpbin.org/get", timeout=5)
            self.response_text.delete("1.0", tk.END)
            if response.status_code == 200:
                self.response_text.insert(tk.END, "Internet Connection Successful!\n")
                self.response_text.insert(tk.END, response.text)
                self.app.update_status("Internet Connection: Successful.")
            else:
                self.response_text.insert(tk.END, "Internet Connection Failed!")
                self.app.update_status("Internet Connection: Failed.")
        except Exception as e:
            self.response_text.delete("1.0", tk.END)
            self.response_text.insert(tk.END, f"Error: {e}")
            self.app.update_status("Internet Connection: Error encountered.")
            
    def send_data(self):
        data = {"simulation": "The Eternal Zahoor Simulator", "status": "Test data"}
        try:
            response = requests.post("https://httpbin.org/post", json=data, timeout=5)
            self.response_text.delete("1.0", tk.END)
            if response.status_code == 200:
                self.response_text.insert(tk.END, "Data sent successfully!\n")
                self.response_text.insert(tk.END, response.text)
                self.app.update_status("Data sent to server successfully.")
            else:
                self.response_text.insert(tk.END, "Failed to send data!")
                self.app.update_status("Failed to send data to server.")
        except Exception as e:
            self.response_text.delete("1.0", tk.END)
            self.response_text.insert(tk.END, f"Error: {e}")
            self.app.update_status("Error sending data to server.")

# ==================== Tab 7: Tutorial ====================
class TutorialTab:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        tk.Label(parent, text="Tutorial & Documentation", font=("Arial", 16, "bold")).pack(pady=10)
        tutorial_text = (
            "Welcome to The Eternal Zahoor Simulator!\n\n"
            "This app simulates mass-energy conversion using Einstein's E = m·c² formula.\n\n"
            "Tabs:\n"
            "1. Mass-Energy Conversion: Enter a mass to compute its energy equivalent.\n"
            "2. Advanced Mass Tracker: Run interactive simulations with parameters like reaction rate, temperature, and pressure.\n"
            "   - Use the 'Nuclear Fusion' option for an alternate model.\n"
            "3. Historical Simulation: View a timeline of mass conversion steps.\n"
            "4. Data Logging: Refresh and export simulation data as CSV or JSON.\n"
            "5. 3D Visualization: Explore simulation data in an interactive 3D scatter plot.\n"
            "6. Network Simulation: Check internet connectivity and send simulation data.\n"
            "7. Tutorial: You're here! Read instructions and app usage details.\n\n"
            "Menu Options:\n"
            "   - File > Exit: Close the app.\n"
            "   - Help > About: App information.\n"
            "   - Theme > Toggle Dark Mode: Switch between light and dark themes.\n\n"
            "Enjoy exploring the simulation and learning about mass-energy conversion!"
        )
        self.text_area = tk.Text(parent, wrap="word", font=("Arial", 12), height=20)
        self.text_area.insert("1.0", tutorial_text)
        self.text_area.config(state="disabled")
        self.text_area.pack(pady=10, padx=10, fill="both", expand=True)

# ==================== Main App: Zahoor Simulator ====================
class ZahoorApp:
    def __init__(self, root):
        self.root = root
        root.title("The Eternal Zahoor Simulator - Advanced App")
        root.geometry("1300x950")
        self.create_menu()
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)
        
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.tab3 = ttk.Frame(self.notebook)
        self.tab4 = ttk.Frame(self.notebook)
        self.tab5 = ttk.Frame(self.notebook)
        self.tab6 = ttk.Frame(self.notebook)
        self.tab7 = ttk.Frame(self.notebook)  # Tutorial
        
        self.notebook.add(self.tab1, text="Mass-Energy Conversion")
        self.notebook.add(self.tab2, text="Advanced Mass Tracker")
        self.notebook.add(self.tab3, text="Historical Simulation")
        self.notebook.add(self.tab4, text="Data Logging")
        self.notebook.add(self.tab5, text="3D Visualization")
        self.notebook.add(self.tab6, text="Network Simulation")
        self.notebook.add(self.tab7, text="Tutorial")
        
        self.mass_energy_tab = MassEnergyConversionTab(self.tab1, self)
        self.advanced_tracker_tab = AdvancedMassConservationTrackerTab(self.tab2, self)
        self.historical_tab = HistoricalSimulationTab(self.tab3, self)
        self.data_logging_tab = DataLoggingTab(self.tab4, self.get_historical_data, self)
        self.visualization3d_tab = Visualization3DTab(self.tab5, self.get_historical_data, self)
        self.network_tab = NetworkSimulationTab(self.tab6, self)
        self.tutorial_tab = TutorialTab(self.tab7, self)
        
        self.status_var = tk.StringVar()
        self.status_var.set("Welcome to The Eternal Zahoor Simulator!")
        self.status_bar = tk.Label(root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor='w', font=("Arial", 10))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.apply_theme()
        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        theme_menu = tk.Menu(menubar, tearoff=0)
        theme_menu.add_command(label="Toggle Dark Mode", command=self.toggle_dark_mode)
        menubar.add_cascade(label="Theme", menu=theme_menu)
        self.root.config(menu=menubar)
        
    def show_about(self):
        messagebox.showinfo("About", "The Eternal Zahoor Simulator\nVersion 2.0\nAdvanced multi-functional simulation app.\nDeveloped with Python and Tkinter.")
        
    def update_status(self, msg):
        self.status_var.set(msg)
        
    def get_historical_data(self):
        return self.historical_tab.sim_data
        
    def toggle_dark_mode(self):
        global DARK_MODE
        DARK_MODE = not DARK_MODE
        self.apply_theme()
        mode = "Dark" if DARK_MODE else "Light"
        self.update_status(f"Theme switched to {mode} Mode.")
        
    def apply_theme(self):
        bg_color = "#2e2e2e" if DARK_MODE else "#f0f0f0"
        fg_color = "#ffffff" if DARK_MODE else "#000000" x
        widget_bg = bg_color
        widget_fg = fg_color
        
        self.root.config(bg=bg_color)
        self.status_bar.config(bg=bg_color, fg=fg_color)
        for widget in self.root.winfo_children():
            if isinstance(widget, (tk.Frame, ttk.Frame, tk.Label, tk.Button, tk.Entry, tk.Text)):
                try:
                    widget.config(bg=widget_bg, fg=widget_fg)
                except:
                    pass
        if hasattr(self, 'tutorial_tab'):
            self.tutorial_tab.text_area.config(bg=bg_color, fg=fg_color, insertbackground=fg_color)

def main():
    root = tk.Tk()
    app = ZahoorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
