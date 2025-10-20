# =============================================================================
# Fase 1: Calidad de Datos — Interfaz Moderna + Limpieza Correcta (Ajuste de Ancho de Etiqueta)
# Autor: [Tu Nombre]
# Propósito: Herramienta profesional para ingenieros de petróleo
# =============================================================================

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import os

class CalidadDatosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Herramienta de Calidad de Datos con Rangos")
        self.root.geometry("1200x850")
        self.root.resizable(True, True)

        # Datos
        self.df_prod = None
        self.df_pt = None
        self.df_final = None
        self.df_orig = None  # Para graficar datos originales
        self.all_vars = []
        self.rangos_propuestos = {}
        self.rango_entries = {}

        self.create_widgets()

    def create_widgets(self):
        # Configuración de las columnas y filas principales
        self.root.columnconfigure(0, weight=0) # Columna de botones: ancho fijo
        self.root.columnconfigure(1, weight=1) # Columna central (log, gráficos): se expande
        self.root.rowconfigure(0, weight=1) # Fila principal

        # === Panel Izquierdo: Botones y Rangos (Columna 0) ===
        left_control_frame = ttk.Frame(self.root, padding="10 5")
        left_control_frame.grid(row=0, column=0, sticky="ns", padx=(10,0), pady=10)
        
        # 1. Contenedor de Botones (arriba)
        button_container = ttk.Frame(left_control_frame)
        button_container.pack(fill="x", pady=(0, 10))

        ttk.Button(button_container, text="1. Cargar Datos Producción (prod)", command=lambda: self.cargar_archivo("prod")).pack(fill="x", pady=5)
        ttk.Button(button_container, text="2. Cargar Datos Punto de Toma (pt)", command=lambda: self.cargar_archivo("pt")).pack(fill="x", pady=5)
        ttk.Button(button_container, text="3. Analizar Variables", command=self.analizar_datos).pack(fill="x", pady=5)
        ttk.Button(button_container, text="4. Limpiar Datos", command=self.limpiar_datos).pack(fill="x", pady=5)
        ttk.Button(button_container, text="5. Guardar Datos Limpios", command=self.guardar_datos).pack(fill="x", pady=5)
        
        # 2. Rangos Operativos (debajo de los botones)
        ttk.Label(left_control_frame, text="Rangos Operativos (mín, máx):", font="-weight bold").pack(anchor="w", pady=(10, 5))
        self.rangos_frame = ttk.Frame(left_control_frame)
        self.rangos_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # === Panel Central/Derecho: Log, Selectores, Gráficos (Columna 1) ===
        main_content_frame = ttk.Frame(self.root, padding="10 5")
        main_content_frame.grid(row=0, column=1, sticky="nsew")
        main_content_frame.columnconfigure(0, weight=1)

        # Definición de filas:
        main_content_frame.rowconfigure(0, weight=0) # Fila del Log
        main_content_frame.rowconfigure(1, weight=0) # Fila de Selectores de Gráfico
        main_content_frame.rowconfigure(2, weight=1) # Fila de Gráficos (se expande)
        main_content_frame.rowconfigure(3, weight=0) # Fila del Toolbar

        # ----------------------------------------------------
        # 1. Log de Operaciones (Fila 0)
        # ----------------------------------------------------
        ttk.Label(main_content_frame, text="Log de Operaciones:", font="-weight bold").grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.log = scrolledtext.ScrolledText(main_content_frame, height=5, state="disabled")
        self.log.grid(row=0, column=0, sticky="nsew", pady=(0, 10))

        # ----------------------------------------------------
        # 2. Selectores de variables y botón de actualizar gráfico (Fila 1)
        # ----------------------------------------------------
        select_frame = ttk.Frame(main_content_frame)
        select_frame.grid(row=1, column=0, sticky="ew", pady=(10, 5))

        ttk.Label(select_frame, text="Gráfico 1:").pack(side="left", padx=(0, 5))
        self.var1 = tk.StringVar()
        self.combo1 = ttk.Combobox(select_frame, textvariable=self.var1, state="readonly", width=20)
        self.combo1.pack(side="left", padx=(0, 20))

        ttk.Label(select_frame, text="Gráfico 2:").pack(side="left", padx=(0, 5))
        self.var2 = tk.StringVar()
        self.combo2 = ttk.Combobox(select_frame, textvariable=self.var2, state="readonly", width=20)
        self.combo2.pack(side="left", padx=(0, 10))

        ttk.Button(select_frame, text="📊 Actualizar Gráfico", command=self.actualizar_grafico_manual).pack(side="left")

        # ----------------------------------------------------
        # 3. Área de gráficos (Fila 2)
        # ----------------------------------------------------
        self.fig, self.axs = plt.subplots(2, 1, figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, main_content_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=2, column=0, sticky="nsew")

        # 4. Barra de herramientas de Matplotlib (Fila 3 - Solución TclError)
        toolbar_frame = ttk.Frame(main_content_frame)
        toolbar_frame.grid(row=3, column=0, sticky="ew", pady=(5,0))
        
        self.toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        self.toolbar.update()
        self.toolbar.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Ajustar la figura para un mejor diseño inicial
        for ax in self.axs:
            ax.clear()
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_frame_on(True)
            ax.set_title("Cargue y limpie datos para visualizar")
        self.fig.tight_layout()
        self.canvas.draw()


    def log_message(self, msg):
        self.log.config(state="normal")
        self.log.insert(tk.END, msg + "\n")
        self.log.config(state="disabled")
        self.log.see(tk.END)

    def cargar_archivo(self, tipo):
        file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file:
            return
        try:
            df = pd.read_csv(
                file,
                sep=';',
                na_values=["NULL", "null", "N/A", "n/a", "#N/A", "", "NaN", "nan"],
                keep_default_na=True,
                decimal=',',
                dayfirst=True,
                encoding='utf-8'
            )

            fecha_col = None
            for col in df.columns:
                if str(col).strip().upper() == 'FECHA':
                    fecha_col = col
                    break

            if fecha_col is None:
                cols = [str(c).strip() for c in df.columns]
                messagebox.showerror("Error", f"Columnas detectadas: {cols}\n\nDebe haber una columna 'FECHA'.")
                return

            df.rename(columns={fecha_col: 'Fecha'}, inplace=True)
            df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
            if df['Fecha'].isnull().any():
                self.log_message("⚠️ Advertencia: Algunas fechas no pudieron convertirse.")

            if tipo == "prod":
                self.df_prod = df
                self.log_message(f"✅ Archivo 1 cargado: {os.path.basename(file)}")
            else:
                self.df_pt = df
                self.log_message(f"✅ Archivo 2 cargado: {os.path.basename(file)}")

        except Exception as e:
            messagebox.showerror("Error", f"Detalles:\n{e}")

    def analizar_datos(self):
        if self.df_prod is None and self.df_pt is None:
            messagebox.showwarning("Advertencia", "Carga al menos un archivo.")
            return

        dfs = [df for df in [self.df_prod, self.df_pt] if df is not None]
        if len(dfs) == 1:
            df_comb = dfs[0].set_index('Fecha')
        else:
            df_comb = pd.merge(dfs[0], dfs[1], on='Fecha', how='outer').set_index('Fecha')
        df_comb = df_comb.sort_index()

        self.all_vars = []
        for col in df_comb.columns:
            if col == 'Fecha':
                continue
            serie_num = pd.to_numeric(df_comb[col], errors='coerce')
            if serie_num.notnull().sum() > 0:
                self.all_vars.append(col)
                df_comb[col] = serie_num

        if not self.all_vars:
            messagebox.showwarning("Advertencia", "No se encontraron variables numéricas.")
            return

        self.rangos_propuestos = {}
        for col in self.all_vars:
            serie = df_comb[col].dropna()
            serie = serie[serie >= 0]
            if len(serie) > 10:
                p1, p99 = np.percentile(serie, [1, 99])
                self.rangos_propuestos[col] = (max(0, round(p1, 2)), round(p99, 2))
            elif len(serie) > 0:
                self.rangos_propuestos[col] = (max(0, serie.min()), serie.max())
            else:
                self.rangos_propuestos[col] = (0, 100)

        for widget in self.rangos_frame.winfo_children():
            widget.destroy()
        self.rango_entries = {}

        for var in sorted(self.all_vars):
            min_r, max_r = self.rangos_propuestos[var]
            frame = ttk.Frame(self.rangos_frame)
            frame.pack(fill="x", pady=1)
            
            # === AJUSTE CLAVE AQUÍ: Aumentamos el ancho a 25 ===
            ttk.Label(frame, text=var, width=25, anchor="w").pack(side="left")
            
            min_entry = ttk.Entry(frame, width=10)
            min_entry.insert(0, str(min_r))
            min_entry.pack(side="left", padx=2)
            max_entry = ttk.Entry(frame, width=10)
            max_entry.insert(0, str(max_r))
            max_entry.pack(side="left", padx=2)
            self.rango_entries[var] = (min_entry, max_entry)

        self.log_message(f"📊 Detectadas {len(self.all_vars)} variables.")
        self.log_message("✅ Rangos listos para ajuste.")

    def limpiar_datos(self,):
        if not self.rango_entries:
            messagebox.showwarning("Advertencia", "Primero analiza los datos.")
            return

        rangos_usar = {}
        for var, (min_e, max_e) in self.rango_entries.items():
            try:
                min_val = float(min_e.get())
                max_val = float(max_e.get())
                if min_val > max_val:
                    raise ValueError("Mínimo > Máximo")
                rangos_usar[var] = (min_val, max_val)
            except ValueError as e:
                messagebox.showerror("Error", f"Rango inválido para '{var}': {e}")
                return

        dfs_orig = []
        if self.df_prod is not None:
            df_temp = self.df_prod.copy()
            for col in df_temp.columns:
                if col != 'Fecha':
                    df_temp[col] = pd.to_numeric(df_temp[col], errors='coerce')
            dfs_orig.append(df_temp.set_index('Fecha'))
        if self.df_pt is not None:
            df_temp = self.df_pt.copy()
            for col in df_temp.columns:
                if col != 'Fecha':
                    df_temp[col] = pd.to_numeric(df_temp[col], errors='coerce')
            dfs_orig.append(df_temp.set_index('Fecha'))

        if len(dfs_orig) == 1:
            self.df_orig = dfs_orig[0].sort_index()
        else:
            self.df_orig = pd.merge(dfs_orig[0], dfs_orig[1], on='Fecha', how='outer').sort_index()

        idx_completo = pd.date_range(start=self.df_orig.index.min(), end=self.df_orig.index.max(), freq='D')
        df_limpio = pd.DataFrame(index=idx_completo)

        for var in self.all_vars:
            if var in self.df_orig.columns:
                min_r, max_r = rangos_usar[var]
                serie = self.df_orig[var].copy()
                # === FILTRADO CORRECTO (NO CLAMPING) ===
                serie = serie[(serie >= min_r) & (serie <= max_r)]
                df_limpio[var] = serie.asfreq('D').interpolate(limit=3)

        self.df_final = df_limpio.reset_index()
        self.df_final.rename(columns={'index': 'Fecha'}, inplace=True)

        # Actualizar selectores
        self.combo1['values'] = self.all_vars
        self.combo2['values'] = self.all_vars
        if self.all_vars:
            self.var1.set(self.all_vars[0])
            if len(self.all_vars) > 1:
                self.var2.set(self.all_vars[1])
            else:
                self.var2.set(self.all_vars[0])
        else:
            self.var1.set("")
            self.var2.set("")

        self.actualizar_grafico_manual()

        self.log_message("✅ Limpieza completada.")
        for col in self.df_final.columns:
            if col != 'Fecha':
                cobertura = 100 * (1 - self.df_final[col].isnull().sum() / len(self.df_final))
                self.log_message(f"   {col}: cobertura = {cobertura:.1f}%")

    def actualizar_grafico_manual(self):
        if self.df_final is None or self.df_orig is None:
            # Limpiar gráficos si no hay datos finales
            for ax in self.axs:
                ax.clear()
                ax.set_xticks([])
                ax.set_yticks([])
                ax.set_frame_on(True)
                ax.set_title("Cargue y limpie datos para visualizar")
            self.fig.tight_layout()
            self.canvas.draw()
            return

        var1 = self.var1.get()
        var2 = self.var2.get()

        for ax in self.axs:
            ax.clear()

        df_final_idx = self.df_final.set_index('Fecha')

        for i, (var, ax) in enumerate(zip([var1, var2], self.axs)):
            if var in self.df_orig.columns and var in df_final_idx.columns:
                ax.plot(self.df_orig.index, self.df_orig[var], 'lightgray', label='Original')
                ax.plot(df_final_idx.index, df_final_idx[var], 'b-o', markersize=2, label='Limpio')
                ax.set_title(f"{var}: Antes vs Después")
                ax.legend()
                ax.grid(True)
            else:
                ax.set_title(f"Gráfico {i+1}: Seleccione una variable válida")
                ax.set_xticks([])
                ax.set_yticks([])
                ax.set_frame_on(False)

        self.fig.tight_layout()
        self.canvas.draw()

    def guardar_datos(self):
        if self.df_final is None:
            messagebox.showwarning("Advertencia", "Primero limpia los datos.")
            return
        file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file:
            self.df_final.to_csv(file, index=False, na_rep='', decimal='.')
            self.log_message(f"💾 Datos guardados: {file}")

if __name__ == "__main__":
    # Configuración de Tkinter para un estilo moderno
    root = tk.Tk()
    root.style = ttk.Style()
    root.style.theme_use("clam")
    
    app = CalidadDatosApp(root)
    root.mainloop()