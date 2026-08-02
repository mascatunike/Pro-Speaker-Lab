import sys
import os
import math
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ----------------------------------------------------------------------
# 1. Generator Schema SVG
# ----------------------------------------------------------------------

class SVGGenerator:
    @staticmethod
    def generate_crossover_svg(pw_tot, imp_w, imp_t, fc1, components, bulb_watts, bulb_code, ways=2, imp_m=8, fc2=0):
        if ways == 1:
            title = f"Conexiune Directa Incinta 1 Cale ({pw_tot}W RMS)"
            return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 250" width="100%" height="100%">
  <rect width="800" height="250" fill="#181818" rx="10" />
  <text x="400" y="30" fill="#ffffff" font-family="Arial" font-size="16" text-anchor="middle" font-weight="bold">{title}</text>
  <circle cx="40" cy="100" r="5" fill="#4caf50"/><text x="15" y="105" fill="#4caf50" font-family="Arial" font-size="12" font-weight="bold">IN +</text>
  <circle cx="40" cy="180" r="5" fill="#f44336"/><text x="15" y="185" fill="#f44336" font-family="Arial" font-size="12" font-weight="bold">IN -</text>
  <path d="M 40 100 L 600 100" stroke="#4caf50" stroke-width="2.5"/>
  <path d="M 40 180 L 600 180" stroke="#f44336" stroke-width="2.5"/>
  <rect x="600" y="85" width="140" height="110" fill="#2b2b2b" stroke="#ff9800" stroke-width="2" rx="3"/>
  <text x="670" y="145" fill="#ffffff" font-family="Arial" font-size="14" text-anchor="middle" font-weight="bold">Woofer ({imp_w} Ω)</text>
</svg>"""

        title = f"Schema Crossover Reala {ways} Cai ({pw_tot}W RMS)"
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 550" width="100%" height="100%">
  <rect width="800" height="550" fill="#181818" rx="10" />
  <text x="400" y="30" fill="#ffffff" font-family="Arial" font-size="16" text-anchor="middle" font-weight="bold">{title}</text>
  <circle cx="40" cy="100" r="5" fill="#4caf50"/>
  <text x="15" y="105" fill="#4caf50" font-family="Arial" font-size="12" font-weight="bold">IN +</text>
  <circle cx="40" cy="500" r="5" fill="#f44336"/>
  <text x="15" y="505" fill="#f44336" font-family="Arial" font-size="12" font-weight="bold">IN -</text>
  <path d="M 40 500 L 760 500" stroke="#f44336" stroke-width="2.5" fill="none"/>
"""
        lw, cw = components['L_w'], components['C_w']
        ct, lt = components['C_t'], components['L_t']
        rz, cz = components['R_z'], components['C_z']
        r1, r2 = components['R1_lpad'], components['R2_lpad']
        
        svg += f"""
  <path d="M 40 100 L 80 100" stroke="#4caf50" stroke-width="2.5"/>
  <circle cx="80" cy="100" r="4" fill="#4caf50"/>
  <path d="M 80 100 L 80 70 L 110 70" stroke="#4caf50" stroke-width="2" fill="none"/>

  <!-- Ct Serie (Tweeter) -->
  <line x1="110" y1="60" x2="110" y2="80" stroke="#2196f3" stroke-width="3"/>
  <line x1="120" y1="60" x2="120" y2="80" stroke="#2196f3" stroke-width="3"/>
  <text x="115" y="48" fill="#2196f3" font-family="Arial" font-size="10" font-weight="bold" text-anchor="middle">Ct={ct:.2f}uF</text>
  <path d="M 120 70 L 210 70" stroke="#4caf50" stroke-width="2"/>
  <circle cx="210" cy="70" r="3" fill="#4caf50"/>
  
  <!-- Lt Paralel (Tweeter) -->
  <path d="M 210 70 L 210 90" stroke="#4caf50" stroke-width="2"/>
  <path d="M 210 90 Q 195 100 210 110 Q 195 120 210 130 Q 195 140 210 150" stroke="#2196f3" stroke-width="2.5" fill="none"/>
  <path d="M 210 150 L 210 500" stroke="#f44336" stroke-width="2"/>
  <text x="235" y="120" fill="#2196f3" font-family="Arial" font-size="10" font-weight="bold">Lt={lt:.2f}mH</text>

  <!-- PROTECTIE BEC 12V -->
  <path d="M 210 70 L 260 70" stroke="#4caf50" stroke-width="2"/>
  <rect x="260" y="52" width="65" height="36" fill="#fbc02d" stroke="#fff" stroke-width="1.5" rx="5"/>
  <text x="292" y="66" fill="#000" font-family="Arial" font-size="9" font-weight="bold" text-anchor="middle">BEC 12V</text>
  <text x="292" y="80" fill="#000" font-family="Arial" font-size="8" font-weight="bold" text-anchor="middle">{bulb_watts}W ({bulb_code.split('/')[0]})</text>
  <path d="M 325 70 L 370 70" stroke="#4caf50" stroke-width="2"/>

  <!-- L-PAD -->
  <rect x="370" y="60" width="40" height="20" fill="none" stroke="#9c27b0" stroke-width="2"/>
  <text x="390" y="52" fill="#9c27b0" font-family="Arial" font-size="10" font-weight="bold" text-anchor="middle">R1={r1:.1f}Ω</text>
  <path d="M 410 70 L 480 70" stroke="#4caf50" stroke-width="2"/>
  <circle cx="480" cy="70" r="3" fill="#4caf50"/>

  <path d="M 480 70 L 480 90" stroke="#4caf50" stroke-width="2"/>
  <rect x="470" y="90" width="20" height="40" fill="none" stroke="#9c27b0" stroke-width="2"/>
  <text x="515" y="115" fill="#9c27b0" font-family="Arial" font-size="10" font-weight="bold">R2={r2:.1f}Ω</text>
  <path d="M 480 130 L 480 500" stroke="#f44336" stroke-width="2"/>

  <!-- Tweeter Out -->
  <path d="M 480 70 L 600 70" stroke="#4caf50" stroke-width="2"/>
  <rect x="600" y="55" width="110" height="30" fill="#2b2b2b" stroke="#2196f3" stroke-width="2" rx="3"/>
  <text x="655" y="74" fill="#ffffff" font-family="Arial" font-size="11" text-anchor="middle" font-weight="bold">Tweeter ({imp_t} Ω)</text>
  <path d="M 710 70 L 730 70 L 730 500" stroke="#f44336" stroke-width="2" fill="none"/>
"""

        if ways == 3:
            c_m1, l_m1 = components.get('C_m1', 0), components.get('L_m1', 0)
            svg += f"""
  <!-- Midrange Branch -->
  <path d="M 80 100 L 80 230 L 110 230" stroke="#4caf50" stroke-width="2" fill="none"/>
  <line x1="110" y1="220" x2="110" y2="240" stroke="#00e676" stroke-width="3"/>
  <line x1="120" y1="220" x2="120" y2="240" stroke="#00e676" stroke-width="3"/>
  <text x="115" y="205" fill="#00e676" font-family="Arial" font-size="10" font-weight="bold" text-anchor="middle">Cm={c_m1:.1f}uF</text>
  <text x="115" y="220" fill="#00e676" font-family="Arial" font-size="10" font-weight="bold" text-anchor="middle">Lm={l_m1:.2f}mH</text>

  <path d="M 120 230 L 600 230" stroke="#4caf50" stroke-width="2"/>
  <rect x="600" y="215" width="110" height="30" fill="#2b2b2b" stroke="#00e676" stroke-width="2" rx="3"/>
  <text x="655" y="234" fill="#ffffff" font-family="Arial" font-size="11" text-anchor="middle" font-weight="bold">Midrange ({imp_m} Ω)</text>
  <path d="M 710 230 L 730 230 L 730 500" stroke="#f44336" stroke-width="2" fill="none"/>
"""

        y_w = 380 if ways == 3 else 240
        svg += f"""
  <!-- Lw Serie (Woofer) -->
  <path d="M 80 100 L 80 {y_w} L 110 {y_w}" stroke="#4caf50" stroke-width="2" fill="none"/>
  <path d="M 110 {y_w} Q 125 {y_w-15} 140 {y_w} Q 155 {y_w-15} 170 {y_w} Q 185 {y_w-15} 200 {y_w}" stroke="#ff9800" stroke-width="3.5" fill="none"/>
  <text x="155" y="{y_w-25}" fill="#ff9800" font-family="Arial" font-size="10" font-weight="bold" text-anchor="middle">Lw={lw:.2f}mH</text>
  <path d="M 200 {y_w} L 300 {y_w}" stroke="#4caf50" stroke-width="2"/>
  <circle cx="300" cy="{y_w}" r="3" fill="#4caf50"/>

  <!-- Cw Paralel (Woofer) -->
  <path d="M 300 {y_w} L 300 {y_w+20}" stroke="#4caf50" stroke-width="2"/>
  <line x1="290" y1="{y_w+20}" x2="310" y2="{y_w+20}" stroke="#ff9800" stroke-width="3"/>
  <line x1="290" y1="{y_w+30}" x2="310" y2="{y_w+30}" stroke="#ff9800" stroke-width="3"/>
  <path d="M 300 {y_w+30} L 300 500" stroke="#f44336" stroke-width="2"/>
  <text x="335" y="{y_w+30}" fill="#ff9800" font-family="Arial" font-size="10" font-weight="bold">Cw={cw:.1f}uF</text>

  <!-- ZOBEL -->
  <path d="M 300 {y_w} L 480 {y_w}" stroke="#4caf50" stroke-width="2"/>
  <circle cx="480" cy="{y_w}" r="3" fill="#4caf50"/>
  <rect x="470" y="{y_w+15}" width="20" height="25" fill="none" stroke="#e91e63" stroke-width="2"/>
  <path d="M 480 {y_w} L 480 {y_w+15} M 480 {y_w+40} L 480 {y_w+55}" stroke="#4caf50" stroke-width="2"/>
  <line x1="470" y1="{y_w+55}" x2="490" y2="{y_w+55}" stroke="#e91e63" stroke-width="3"/>
  <line x1="470" y1="{y_w+65}" x2="490" y2="{y_w+65}" stroke="#e91e63" stroke-width="3"/>
  <path d="M 480 {y_w+65} L 480 500" stroke="#f44336" stroke-width="2"/>
  <text x="515" y="{y_w+28}" fill="#e91e63" font-family="Arial" font-size="10" font-weight="bold">Rz={rz:.1f}Ω</text>
  <text x="515" y="{y_w+63}" fill="#e91e63" font-family="Arial" font-size="10" font-weight="bold">Cz={cz:.1f}uF</text>

  <!-- Woofer Out -->
  <path d="M 480 {y_w} L 600 {y_w}" stroke="#4caf50" stroke-width="2"/>
  <rect x="600" y="{y_w-15}" width="110" height="30" fill="#2b2b2b" stroke="#ff9800" stroke-width="2" rx="3"/>
  <text x="655" y="{y_w+4}" fill="#ffffff" font-family="Arial" font-size="11" text-anchor="middle" font-weight="bold">Woofer ({imp_w} Ω)</text>
  <path d="M 710 {y_w} L 730 {y_w} L 730 500" stroke="#f44336" stroke-width="2" fill="none"/>

  <rect x="40" y="515" width="720" height="25" fill="#222" rx="5" stroke="#444"/>
  <text x="400" y="532" fill="#4caf50" font-family="Arial" font-size="11" text-anchor="middle" font-weight="bold">Filtru Crossover Pro Speaker Lab | Software BY_M@$K</text>
</svg>"""
        return svg

# ----------------------------------------------------------------------
# 2. Generator Grafic Răspuns în Frecvență
# ----------------------------------------------------------------------

class FrequencyResponsePlotter:
    @staticmethod
    def plot_response(fc1, z_w_fc, z_t_fc, L_w, C_w, L_t, C_t, parent_frame, ways=2, fc2=0, z_m_fc=8, components=None):
        freqs = np.logspace(1, 4.7, 500)
        omega = 2 * np.pi * freqs
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 4.2), sharex=True, facecolor='#2b2b2b')
        for ax in (ax1, ax2):
            ax.set_facecolor('#1e1e1e')
            ax.grid(True, which='both', color='#444444', linestyle='--', linewidth=0.5)
            ax.tick_params(colors='white')

        if ways == 1:
            ax1.semilogx(freqs, np.zeros_like(freqs), label='Woofer / Subwoofer (Direct)', color='#ff9800', linewidth=2)
            ax2.semilogx(freqs, np.zeros_like(freqs), color='#ff9800', linestyle='--', linewidth=1.5)
            title_txt = "Răspuns Incintă 1 Cale (Direct, fără filtru)"
        elif ways == 2:
            L_w_h, C_w_f = L_w / 1000.0, C_w / 1e6
            H_lp = 1 / (1 + 1j*omega*L_w_h/z_w_fc + (1j*omega)**2 * L_w_h * C_w_f)

            L_t_h, C_t_f = L_t / 1000.0, C_t / 1e6
            H_hp = ((1j*omega)**2 * L_t_h * C_t_f) / (1 + 1j*omega*L_t_h/z_t_fc + (1j*omega)**2 * L_t_h * C_t_f)

            ax1.semilogx(freqs, 20 * np.log10(np.abs(H_lp) + 1e-12), label='Woofer (12dB/oct)', color='#ff9800', linewidth=2)
            ax1.semilogx(freqs, 20 * np.log10(np.abs(H_hp) + 1e-12), label='Tweeter (12dB/oct)', color='#2196f3', linewidth=2)
            
            ax2.semilogx(freqs, np.angle(H_lp, deg=True), color='#ff9800', linestyle='--', linewidth=1.5)
            ax2.semilogx(freqs, np.angle(H_hp, deg=True), color='#2196f3', linestyle='--', linewidth=1.5)
            title_txt = f"Răspuns Filtru 2 Căi (Fc = {fc1:.0f} Hz)"
        else: # 3 cai
            L_w_h, C_w_f = L_w / 1000.0, C_w / 1e6
            H_lp = 1 / (1 + 1j*omega*L_w_h/z_w_fc + (1j*omega)**2 * L_w_h * C_w_f)

            L_t_h, C_t_f = L_t / 1000.0, C_t / 1e6
            H_hp = ((1j*omega)**2 * L_t_h * C_t_f) / (1 + 1j*omega*L_t_h/z_t_fc + (1j*omega)**2 * L_t_h * C_t_f)

            f_mid_center = math.sqrt(fc1 * fc2) if fc2 > 0 else fc1
            bw = max(100.0, fc2 - fc1)
            H_bp = (1j*omega*(bw*2*np.pi)) / ((1j*omega)**2 + 1j*omega*(bw*2*np.pi) + (2*np.pi*f_mid_center)**2)

            ax1.semilogx(freqs, 20 * np.log10(np.abs(H_lp) + 1e-12), label='Woofer', color='#ff9800', linewidth=2)
            ax1.semilogx(freqs, 20 * np.log10(np.abs(H_bp) + 1e-12), label='Midrange', color='#00e676', linewidth=2)
            ax1.semilogx(freqs, 20 * np.log10(np.abs(H_hp) + 1e-12), label='Tweeter', color='#2196f3', linewidth=2)

            ax2.semilogx(freqs, np.angle(H_lp, deg=True), color='#ff9800', linestyle='--', linewidth=1.5)
            ax2.semilogx(freqs, np.angle(H_bp, deg=True), color='#00e676', linestyle='--', linewidth=1.5)
            ax2.semilogx(freqs, np.angle(H_hp, deg=True), color='#2196f3', linestyle='--', linewidth=1.5)
            title_txt = f"Răspuns Filtru 3 Căi (Fc1 = {fc1:.0f} Hz, Fc2 = {fc2:.0f} Hz)"

        ax1.set_ylabel('Amplitudine (dB)', color='white')
        ax1.set_ylim(-35, 2)
        ax1.legend(facecolor='#2b2b2b', labelcolor='white')
        ax1.set_title(title_txt, color='white')

        ax2.set_xlabel('Frecvență (Hz)', color='white')
        ax2.set_ylabel('Fază (grade)', color='white')

        fig.tight_layout()
        for widget in parent_frame.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# ----------------------------------------------------------------------
# 3. Interfața Grafică Principală Tkinter
# ----------------------------------------------------------------------

class SpeakerFilterDesigner(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Pro Speaker Lab v5.4 - Created BY_M@$K")
        self.geometry("1060x880")
        self.configure(bg="#181818")
        
        # Variabile Configurare Sistem
        self.ways_var = tk.StringVar(value="2")
        self.p_tot_var = tk.DoubleVar(value=300.0)
        self.fc1_var = tk.DoubleVar(value=2500.0)
        self.fc2_var = tk.DoubleVar(value=5000.0)
        self.box_type_var = tk.StringVar(value="Bass-Reflex")
        self.mdf_thick_var = tk.DoubleVar(value=18.0)

        # Variabile Woofer (Thiele-Small)
        self.imp_w_var = tk.DoubleVar(value=8.0)
        self.re_w_var = tk.DoubleVar(value=6.2)
        self.le_w_var = tk.DoubleVar(value=0.9)
        self.fs_w_var = tk.DoubleVar(value=40.0)
        self.qts_w_var = tk.DoubleVar(value=0.38)
        self.vas_w_var = tk.DoubleVar(value=45.0)
        self.sens_w_var = tk.DoubleVar(value=90.0)

        # Variabile Midrange
        self.imp_m_var = tk.DoubleVar(value=8.0)
        self.sens_m_var = tk.DoubleVar(value=91.0)
        self.p_m_var = tk.DoubleVar(value=80.0)
        
        # Variabile Tweeter
        self.imp_t_var = tk.DoubleVar(value=8.0)
        self.p_t_var = tk.DoubleVar(value=40.0)
        self.sens_t_var = tk.DoubleVar(value=94.0)
        
        self.calc_results = {}
        self.report_text_data = ""
        
        self.setup_styles()
        self.create_widgets()
        
        # Ascultă schimbările numărului de căi
        self.ways_var.trace_add("write", self.on_ways_change)
        self.on_ways_change()

    def setup_styles(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure(".", background="#181818", foreground="#ffffff", fieldbackground="#2b2b2b")
        style.configure("TNotebook", background="#181818", borderwidth=0)
        style.configure("TNotebook.Tab", background="#2b2b2b", foreground="#ffffff", padding=[12, 6])
        style.map("TNotebook.Tab", background=[("selected", "#3a3a3a")], foreground=[("selected", "#00e676")])
        style.configure("TLabelframe", background="#181818", foreground="#00e676", borderwidth=1)
        style.configure("TLabelframe.Label", background="#181818", foreground="#00e676", font=("Arial", 10, "bold"))
        style.configure("TButton", background="#00e676", foreground="#000000", font=("Arial", 10, "bold"))

    def create_widgets(self):
        # Header Principal
        header = ttk.Frame(self)
        header.pack(fill=tk.X, padx=10, pady=10)
        tk.Label(header, text="PRO SPEAKER LAB v5.4", font=("Arial", 16, "bold"), fg="#00e676", bg="#181818").pack(side=tk.LEFT)
        
        btn_site = tk.Button(header, text="🌐 Pagina Oficială", font=("Arial", 9, "bold"), bg="#2196f3", fg="#ffffff", bd=0, padx=10, pady=4, cursor="hand2", command=self.open_website)
        btn_site.pack(side=tk.RIGHT)

        # Tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.tab_inputs = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_inputs, text=" Parametri T/S & Configurare ")
        self.build_inputs_tab()

        self.tab_results = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_results, text=" Rezultate & Dimensiuni MDF ")
        self.build_results_tab()

        self.tab_freq = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_freq, text=" Grafic Răspuns Filtru ")
        
        self.tab_export = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_export, text=" Export / Salvare ")
        self.build_export_tab()

        self.tab_about = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_about, text=" Licență & Despre ")
        self.build_about_tab()

        btn_calc = ttk.Button(self, text="GENEREAZĂ PROIECT COMPLET (FILTRU + INCINTĂ)", command=self.run_calculations)
        btn_calc.pack(fill=tk.X, padx=15, pady=5)

        # FOOTER CREDITS DISCRET JOS
        footer = tk.Frame(self, bg="#101010", height=25)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        
        lbl_copy = tk.Label(footer, text="Creat de BY_M@$K | Toate drepturile rezervate © 2026", font=("Arial", 9, "bold"), fg="#888888", bg="#101010")
        lbl_copy.pack(side=tk.LEFT, padx=15)

        lbl_link = tk.Label(footer, text="https://softuri-mascatunike.duckdns.org", font=("Arial", 9, "underline"), fg="#00e676", bg="#101010", cursor="hand2")
        lbl_link.pack(side=tk.RIGHT, padx=15)
        lbl_link.bind("<Button-1>", lambda e: self.open_website())

    def open_website(self):
        webbrowser.open_new("https://softuri-mascatunike.duckdns.org")

    def build_inputs_tab(self):
        gen_frame = ttk.LabelFrame(self.tab_inputs, text=" Configurație Sistem & Material Incintă ")
        gen_frame.pack(fill=tk.X, padx=15, pady=5)

        ttk.Label(gen_frame, text="Număr Căi:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=3)
        ttk.Combobox(gen_frame, textvariable=self.ways_var, values=["1", "2", "3"], state="readonly", width=8).grid(row=0, column=1, padx=10, pady=3)

        ttk.Label(gen_frame, text="Putere Totală Sistem (Watts RMS):").grid(row=0, column=2, sticky=tk.W, padx=10, pady=3)
        ttk.Entry(gen_frame, textvariable=self.p_tot_var, width=10).grid(row=0, column=3, padx=10, pady=3)

        self.lbl_fc1 = ttk.Label(gen_frame, text="Frecvență Crossover Fc1 (Hz):")
        self.lbl_fc1.grid(row=1, column=0, sticky=tk.W, padx=10, pady=3)
        self.ent_fc1 = ttk.Entry(gen_frame, textvariable=self.fc1_var, width=10)
        self.ent_fc1.grid(row=1, column=1, padx=10, pady=3)

        self.lbl_fc2 = ttk.Label(gen_frame, text="Frecvență Crossover Fc2 (Hz):")
        self.lbl_fc2.grid(row=1, column=2, sticky=tk.W, padx=10, pady=3)
        self.ent_fc2 = ttk.Entry(gen_frame, textvariable=self.fc2_var, width=10)
        self.ent_fc2.grid(row=1, column=3, padx=10, pady=3)

        ttk.Label(gen_frame, text="Tip Incintă:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=3)
        ttk.Combobox(gen_frame, textvariable=self.box_type_var, values=["Bass-Reflex", "Sealed (Închisă)"], state="readonly", width=12).grid(row=2, column=1, padx=10, pady=3)

        ttk.Label(gen_frame, text="Grosime Lemn/MDF (mm):").grid(row=2, column=2, sticky=tk.W, padx=10, pady=3)
        ttk.Entry(gen_frame, textvariable=self.mdf_thick_var, width=10).grid(row=2, column=3, padx=10, pady=3)

        # Frame Woofer
        self.w_frame = ttk.LabelFrame(self.tab_inputs, text=" Parametri Thiele-Small Woofer (Bas) ")
        self.w_frame.pack(fill=tk.X, padx=15, pady=5)

        ttk.Label(self.w_frame, text="Impedanță Nominală Z (Ohm):").grid(row=0, column=0, sticky=tk.W, padx=10, pady=3)
        ttk.Entry(self.w_frame, textvariable=self.imp_w_var, width=8).grid(row=0, column=1, padx=10, pady=3)

        ttk.Label(self.w_frame, text="Rezistență C.C. Re (Ohm):").grid(row=0, column=2, sticky=tk.W, padx=10, pady=3)
        ttk.Entry(self.w_frame, textvariable=self.re_w_var, width=8).grid(row=0, column=3, padx=10, pady=3)

        ttk.Label(self.w_frame, text="Inductanță Le (mH):").grid(row=1, column=0, sticky=tk.W, padx=10, pady=3)
        ttk.Entry(self.w_frame, textvariable=self.le_w_var, width=8).grid(row=1, column=1, padx=10, pady=3)

        ttk.Label(self.w_frame, text="Frecvență Rezonanță Fs (Hz):").grid(row=1, column=2, sticky=tk.W, padx=10, pady=3)
        ttk.Entry(self.w_frame, textvariable=self.fs_w_var, width=8).grid(row=1, column=3, padx=10, pady=3)

        ttk.Label(self.w_frame, text="Factor Calitate Qts:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=3)
        ttk.Entry(self.w_frame, textvariable=self.qts_w_var, width=8).grid(row=2, column=1, padx=10, pady=3)

        ttk.Label(self.w_frame, text="Volum Echivalent Vas (Litri):").grid(row=2, column=2, sticky=tk.W, padx=10, pady=3)
        ttk.Entry(self.w_frame, textvariable=self.vas_w_var, width=8).grid(row=2, column=3, padx=10, pady=3)

        ttk.Label(self.w_frame, text="Sensibilitate (dB/1W/1m):").grid(row=3, column=0, sticky=tk.W, padx=10, pady=3)
        ttk.Entry(self.w_frame, textvariable=self.sens_w_var, width=8).grid(row=3, column=1, padx=10, pady=3)

        # Frame Midrange
        self.m_frame = ttk.LabelFrame(self.tab_inputs, text=" Parametri Midrange (Medii) ")

        ttk.Label(self.m_frame, text="Impedanță Nominală Z (Ohm):").grid(row=0, column=0, sticky=tk.W, padx=10, pady=3)
        ttk.Entry(self.m_frame, textvariable=self.imp_m_var, width=8).grid(row=0, column=1, padx=10, pady=3)

        ttk.Label(self.m_frame, text="Putere RMS Medii (W):").grid(row=0, column=2, sticky=tk.W, padx=10, pady=3)
        ttk.Entry(self.m_frame, textvariable=self.p_m_var, width=8).grid(row=0, column=3, padx=10, pady=3)

        ttk.Label(self.m_frame, text="Sensibilitate SPL (dB/1W/1m):").grid(row=1, column=0, sticky=tk.W, padx=10, pady=3)
        ttk.Entry(self.m_frame, textvariable=self.sens_m_var, width=8).grid(row=1, column=1, padx=10, pady=3)

        # Frame Tweeter
        self.t_frame = ttk.LabelFrame(self.tab_inputs, text=" Parametri Tweeter (Înalte) ")

        ttk.Label(self.t_frame, text="Impedanță Nominală Z (Ohm):").grid(row=0, column=0, sticky=tk.W, padx=10, pady=3)
        ttk.Entry(self.t_frame, textvariable=self.imp_t_var, width=8).grid(row=0, column=1, padx=10, pady=3)

        ttk.Label(self.t_frame, text="Putere RMS Tweeter (W):").grid(row=0, column=2, sticky=tk.W, padx=10, pady=3)
        ttk.Entry(self.t_frame, textvariable=self.p_t_var, width=8).grid(row=0, column=3, padx=10, pady=3)

        ttk.Label(self.t_frame, text="Sensibilitate SPL (dB/1W/1m):").grid(row=1, column=0, sticky=tk.W, padx=10, pady=3)
        ttk.Entry(self.t_frame, textvariable=self.sens_t_var, width=8).grid(row=1, column=1, padx=10, pady=3)

    def on_ways_change(self, *args):
        ways = str(self.ways_var.get())
        if ways == "1":
            # Ascunde Crossover & Midrange & Tweeter
            self.lbl_fc1.grid_remove()
            self.ent_fc1.grid_remove()
            self.lbl_fc2.grid_remove()
            self.ent_fc2.grid_remove()
            self.m_frame.pack_forget()
            self.t_frame.pack_forget()
        elif ways == "2":
            # Arată Fc1 (Crossover), Woofer + Tweeter, Ascunde Medii
            self.lbl_fc1.grid()
            self.ent_fc1.grid()
            self.lbl_fc1.config(text="Frecvență Crossover Fc (Hz):")
            self.lbl_fc2.grid_remove()
            self.ent_fc2.grid_remove()
            self.m_frame.pack_forget()
            self.t_frame.pack(fill=tk.X, padx=15, pady=5)
        elif ways == "3":
            # Arată tot (Woofer + Medii + Tweeter + Fc1 + Fc2)
            self.lbl_fc1.grid()
            self.ent_fc1.grid()
            self.lbl_fc1.config(text="Fc1 Woofer-Mid (Hz):")
            self.lbl_fc2.grid()
            self.ent_fc2.grid()
            self.lbl_fc2.config(text="Fc2 Mid-Tweeter (Hz):")
            self.m_frame.pack(fill=tk.X, padx=15, pady=5)
            self.t_frame.pack(fill=tk.X, padx=15, pady=5)

    def build_results_tab(self):
        self.results_text = tk.Text(self.tab_results, bg="#101010", fg="#00ff66", font=("Consolas", 10), wrap=tk.WORD)
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def build_export_tab(self):
        btn_frame = ttk.Frame(self.tab_export)
        btn_frame.pack(fill=tk.X, padx=20, pady=20)
        
        ttk.Button(btn_frame, text="1. Descarcă Raport Proiect & Debitare Lemn (.TXT)", command=self.export_txt_report).pack(fill=tk.X, pady=10)
        ttk.Button(btn_frame, text="2. Descarcă Schemă Electrică Crossover (.SVG)", command=self.export_crossover_svg).pack(fill=tk.X, pady=10)

    def build_about_tab(self):
        txt_about = tk.Text(self.tab_about, bg="#121212", fg="#ffffff", font=("Segoe UI", 10), wrap=tk.WORD, padx=15, pady=15)
        txt_about.pack(fill=tk.BOTH, expand=True)

        info_text = """PRO SPEAKER LAB v5.4
Software pentru Proiectare Incinte Acustice & Crossover-e Audio
------------------------------------------------------------------

Dezvoltator Software: BY_M@$K
Pagina Oficială Web: https://softuri-mascatunike.duckdns.org
Toate drepturile rezervate © 2026

==================================================================
ACORD DE LICENȚĂ NON-COMERCIALĂ (NON-COMMERCIAL LICENSE)
==================================================================

1. DREPTURI DE UTILIZARE:
   Acest software este furnizat GRATUIT exclusiv pentru utilizare personală, 
   educațională și non-comercială. 

2. RESTRICȚII COMERCIALE:
   Este strict interzisă vânzarea, închirierea, redistribuirea contra cost sau 
   includerea acestui software în pachete comerciale fără acordul scris al autorului (BY_M@$K).

3. PROPRIETATE INTELECTUALĂ:
   Toate drepturile de autor, mărcile comerciale și drepturile asupra codului sursă 
   aparțin în exclusivitate creatorului BY_M@$K.

4. ABSENȚA GARANȚIEI:
   Software-ul este furnizat "ca atare" (AS IS), fără nicio garanție expresă sau implicită. 
   Autorul nu poartă răspunderea pentru erori de calcul fizic sau daune aduse echipamentelor audio.

Vă mulțumim că folosiți software-ul nostru oficial!
Website: https://softuri-mascatunike.duckdns.org
"""
        txt_about.insert(tk.END, info_text)
        txt_about.config(state=tk.DISABLED)

    def run_calculations(self):
        try:
            ways = int(self.ways_var.get())
            p_tot = self.p_tot_var.get()
            fc1 = self.fc1_var.get()
            fc2 = self.fc2_var.get() if ways == 3 else 0.0
            box_type = self.box_type_var.get()
            mdf_mm = self.mdf_thick_var.get()

            rw, re_w, le_w_mh = self.imp_w_var.get(), self.re_w_var.get(), self.le_w_var.get()
            le_w_h = le_w_mh / 1000.0
            fs, qts, vas = self.fs_w_var.get(), self.qts_w_var.get(), self.vas_w_var.get()
            sens_w = self.sens_w_var.get()

            rm = self.imp_m_var.get() if ways == 3 else 8.0
            sens_m = self.sens_m_var.get() if ways == 3 else 90.0
            p_m = self.p_m_var.get() if ways == 3 else 0.0

            rt = self.imp_t_var.get() if ways >= 2 else 8.0
            p_t_rms = self.p_t_var.get() if ways >= 2 else 40.0
            sens_t = self.sens_t_var.get() if ways >= 2 else 90.0

            xl_w = 2 * math.pi * fc1 * le_w_h
            z_w_fc = math.sqrt((re_w ** 2) + (xl_w ** 2)) if ways > 1 else rw

            att_db = max(0.0, sens_t - sens_w)
            if att_db > 0 and ways >= 2:
                k = 10 ** (att_db / 20.0)
                R1_lpad = rt * (k - 1) / k
                R2_lpad = rt / (k - 1)
                z_t_fc = rt
            else:
                R1_lpad = 0.0
                R2_lpad = 99999.0
                z_t_fc = rt

            components = {}
            if ways >= 2:
                L_w = ((math.sqrt(2) * z_w_fc) / (2 * math.pi * fc1)) * 1000.0
                C_w = (1.0 / (2 * math.pi * fc1 * math.sqrt(2) * z_w_fc)) * 1e6
                
                fc_t = fc2 if ways == 3 else fc1
                C_t = (1.0 / (2 * math.pi * fc_t * math.sqrt(2) * z_t_fc)) * 1e6
                L_t = ((math.sqrt(2) * z_t_fc) / (2 * math.pi * fc_t)) * 1000.0

                R_z = 1.25 * re_w
                C_z = (le_w_h / (R_z ** 2)) * 1e6 if R_z > 0 else 0

                components.update({
                    'L_w': L_w, 'C_w': C_w, 'C_t': C_t, 'L_t': L_t,
                    'R_z': R_z, 'C_z': C_z,
                    'R1_lpad': R1_lpad, 'R2_lpad': R2_lpad
                })

                if ways == 3:
                    C_m1 = (1.0 / (2 * math.pi * fc1 * math.sqrt(2) * rm)) * 1e6
                    L_m1 = ((math.sqrt(2) * rm) / (2 * math.pi * fc1)) * 1000.0
                    C_m2 = (1.0 / (2 * math.pi * fc2 * math.sqrt(2) * rm)) * 1e6
                    L_m2 = ((math.sqrt(2) * rm) / (2 * math.pi * fc2)) * 1000.0
                    components.update({'C_m1': C_m1, 'L_m1': L_m1, 'C_m2': C_m2, 'L_m2': L_m2})
            else:
                L_w = C_w = L_t = C_t = R_z = C_z = 0.0

            if p_t_rms <= 25:
                bulb_watts = 10
                bulb_code = "C10W / Sofit 12V Auto"
            elif p_t_rms <= 65:
                bulb_watts = 21
                bulb_code = "P21W / Semnalizare 12V Auto"
            else:
                bulb_watts = 42
                bulb_code = "2x P21W în Paralel (2x 21W / 12V)"

            if "Bass-Reflex" in box_type:
                v_woofer_liters = 20.0 * (qts ** 3.3) * vas
                fb_port = 0.42 * fs / (qts ** 0.9)
                d_port_cm = 7.5
                r_port_m = (d_port_cm / 2.0) / 100.0
                area_m2 = math.pi * (r_port_m ** 2)
                v_box_m3 = v_woofer_liters / 1000.0
                len_port_cm = ((23540 * area_m2) / ((fb_port ** 2) * v_box_m3)) - (0.825 * d_port_cm)
                len_port_cm = max(3.0, len_port_cm)
                port_info = f"Diametru Tub: {d_port_cm} cm | Lungime Tub: {len_port_cm:.1f} cm"
            else:
                v_woofer_liters = vas / (((0.707 / qts) ** 2) - 1.0) if qts < 0.707 else vas
                fb_port = fs * (0.707 / qts) if qts > 0 else fs
                port_info = "Incintă Închisă (Complet etanșă, fără tub)"

            if ways == 3:
                v_mid_liters = max(4.0, p_m / 10.0)
                port_info_mid = f"Incintă Midrange: Închisă | Volum aproximativ {v_mid_liters:.2f} L"
            else:
                v_mid_liters = 0.0
                port_info_mid = ""

            v_box_liters = v_woofer_liters + v_mid_liters
            v_box_liters = max(4.0, v_box_liters)

            v_cm3 = v_woofer_liters * 1000.0
            w_int = (v_cm3 / 1.12) ** (1/3)
            h_int = 1.6 * w_int
            d_int = 0.7 * w_int

            v_mid_cm3 = v_mid_liters * 1000.0
            w_int_mid = (v_mid_cm3 / 1.12) ** (1/3) if v_mid_liters > 0 else 0.0
            h_int_mid = 1.6 * w_int_mid
            d_int_mid = 0.7 * w_int_mid

            mdf_cm = mdf_mm / 10.0
            w_ext = w_int + (2 * mdf_cm)
            h_ext = h_int + (2 * mdf_cm)
            d_ext = d_int + (2 * mdf_cm)
            w_ext_mid = w_int_mid + (2 * mdf_cm) if ways == 3 else 0.0
            h_ext_mid = h_int_mid + (2 * mdf_cm) if ways == 3 else 0.0
            d_ext_mid = d_int_mid + (2 * mdf_cm) if ways == 3 else 0.0

            self.calc_results = {
                'ways': ways,
                'pw_tot': p_tot, 'fc1': fc1, 'fc2': fc2,
                'imp_w': rw, 'imp_m': rm, 'imp_t': rt,
                'components': components,
                'bulb_watts': bulb_watts, 'bulb_code': bulb_code
            }

            res = f"========================================================================\n"
            res += f"  PROIECT COMPONENTĂ ACUSTICĂ REALĂ ({ways} CĂI - BY_M@$K)\n"
            res += f"========================================================================\n\n"

            if ways == 1:
                res += f"[1. CONFIGURAȚIE SISTEM 1 CALE (FULL-RANGE / SUBWOOFER)]\n"
                res += f"  • Semnalul se conectează DIRECT de la mufe la difuzor (fără filtru).\n\n"
            elif ways == 2:
                res += f"[1. REZULTATE IMPEDANȚE LA FRECVENȚA DE CROSSOVER ({fc1:.0f} Hz)]\n"
                res += f"  • Impedanță Woofer Reală la Fc (Z_w) : {z_w_fc:.2f} Ω (din cauza Le={le_w_mh}mH)\n"
                res += f"  • Impedanță Tweeter Reală la Fc (Z_t): {z_t_fc:.2f} Ω\n\n"

                res += f"[2. RAMURĂ WOOFER / BAS (Filtru Trece-Jos 12dB/oct)]\n"
                res += f"  • Bobină Serie (L_w)       : {L_w:.2f} mH (Miez Ferită / Aer)\n"
                res += f"  • Condensator Paralel (C_w): {C_w:.1f} µF (Bipolar / MKT)\n"
                res += f"  • Rețea Zobel Compensare   : R_z = {R_z:.2f} Ω (10W), C_z = {C_z:.1f} µF\n\n"

                res += f"[3. RAMURĂ TWEETER / ÎNALTE (Filtru Trece-Sus 12dB/oct)]\n"
                res += f"  • Condensator Serie (C_t)  : {C_t:.2f} µF (MKP / Poliester min 250V)\n"
                res += f"  • Bobină Paralel (L_t)     : {L_t:.2f} mH (Aer)\n"
                res += f"  • Protecție Bec 12V        : {bulb_watts}W ({bulb_code})\n"
                if att_db > 0:
                    res += f"  • Atenuare L-Pad (-{att_db:.1f} dB) : R1 = {R1_lpad:.2f} Ω (Serie), R2 = {R2_lpad:.2f} Ω (Paralel)\n\n"
                else:
                    res += f"  • Atenuare L-Pad           : Nu este necesară\n\n"
            else: # 3 Cai
                res += f"[1. REZULTATE CROSSOVER 3 CĂI (Fc1 = {fc1:.0f} Hz, Fc2 = {fc2:.0f} Hz)]\n"
                res += f"  • Woofer Low-Pass          : L_w = {L_w:.2f} mH, C_w = {C_w:.1f} µF\n"
                res += f"  • Midrange Band-Pass       : Cm1 = {components.get('C_m1', 0):.1f} µF, Lm2 = {components.get('L_m2', 0):.2f} mH\n"
                res += f"  • Tweeter High-Pass        : C_t = {C_t:.2f} µF, L_t = {L_t:.2f} mH\n"
                res += f"  • Protecție Bec Tweeter 12V : {bulb_watts}W ({bulb_code})\n\n"

            res += f"[DIMENSIUNI INCINTĂ & LISTĂ TĂIERE MDF ({mdf_mm} mm)]\n"
            if ways == 3:
                res += f"  • Volum Net Necesar Woofer : {v_woofer_liters:.2f} Litri\n"
                res += f"  • Volum Recomandat Midrange: {v_mid_liters:.2f} Litri\n"
                res += f"  • Volum Total Aproximativ : {v_box_liters:.2f} Litri\n"
            else:
                res += f"  • Volum Net Necesar : {v_box_liters:.2f} Litri\n"
            res += f"  • Dimensiuni EXTERIOARE Woofer (H x L x A) : {h_ext:.1f} cm x {w_ext:.1f} cm x {d_ext:.1f} cm\n"
            if ways == 3:
                res += f"  • Dimensiuni EXTERIOARE Midrange (H x L x A) : {h_ext_mid:.1f} cm x {w_ext_mid:.1f} cm x {d_ext_mid:.1f} cm\n"
            res += f"  • Detalii Acordaj   : {port_info}\n"
            if ways == 3:
                res += f"  • {port_info_mid}\n"
            res += f"  • LISTĂ TĂIERE PLĂCI MDF (pentru 1 Boxă Woofer):\n"
            res += f"    - Față / Spate (2 bucăți) : {h_ext:.1f} cm x {w_ext:.1f} cm\n"
            res += f"    - Stânga / Dreapta (2 bucăți) : {h_ext:.1f} cm x {d_int:.1f} cm\n"
            res += f"    - Capac Sus / Jos (2 bucăți) : {w_int:.1f} cm x {d_int:.1f} cm\n"
            if ways == 3:
                res += f"  • LISTĂ TĂIERE PLĂCI MDF MIDRANGE (opțional):\n"
                res += f"    - Față / Spate (2 bucăți) : {h_ext_mid:.1f} cm x {w_ext_mid:.1f} cm\n"
                res += f"    - Stânga / Dreapta (2 bucăți) : {h_ext_mid:.1f} cm x {d_int_mid:.1f} cm\n"
                res += f"    - Capac Sus / Jos (2 bucăți) : {w_int_mid:.1f} cm x {d_int_mid:.1f} cm\n\n"
            else:
                res += f"\n"
            res += f"------------------------------------------------------------------------\n"
            res += f" Software creat de BY_M@$K | https://softuri-mascatunike.duckdns.org\n"

            self.report_text_data = res
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, res)

            FrequencyResponsePlotter.plot_response(
                fc1, z_w_fc, z_t_fc, L_w, C_w, L_t, C_t, 
                self.tab_freq, ways=ways, fc2=fc2, z_m_fc=rm, components=components
            )
            self.notebook.select(self.tab_results)

        except Exception as e:
            messagebox.showerror("Eroare Calcul", f"A apărut o problemă la calcul: {str(e)}")

    def export_txt_report(self):
        if self.report_text_data:
            path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if path:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(self.report_text_data)
                messagebox.showinfo("Salvat", "Raportul a fost salvat cu succes!")
        else:
            messagebox.showwarning("Atenție", "Rulează mai întâi calculul proiectului!")

    def export_crossover_svg(self):
        if self.calc_results:
            path = filedialog.asksaveasfilename(defaultextension=".svg", filetypes=[("SVG Vector", "*.svg")])
            if path:
                svg = SVGGenerator.generate_crossover_svg(
                    self.calc_results['pw_tot'],
                    self.calc_results['imp_w'],
                    self.calc_results['imp_t'],
                    self.calc_results['fc1'],
                    self.calc_results['components'],
                    self.calc_results['bulb_watts'],
                    self.calc_results['bulb_code'],
                    ways=self.calc_results['ways'],
                    imp_m=self.calc_results['imp_m'],
                    fc2=self.calc_results['fc2']
                )
                with open(path, "w", encoding="utf-8") as f:
                    f.write(svg)
                messagebox.showinfo("Salvat", "Schema vectorială SVG a fost exportată!")
        else:
            messagebox.showwarning("Atenție", "Rulează mai întâi calculul proiectului!")

if __name__ == "__main__":
    app = SpeakerFilterDesigner()
    app.mainloop()
