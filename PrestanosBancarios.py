import tkinter as tk
from tkinter import ttk, messagebox

def evaluar_riesgo():
    try:
        puntuacion = int(entry_puntuacion.get())
        ingresos = float(entry_ingresos.get())
        cuota = float(entry_cuota.get())
        dti = float(entry_dti.get())
        tiempo_empleo = int(entry_tiempo_empleo.get())
        garantia = combo_garantia.get()
        historial_prestamos = combo_historial_prestamos.get()
        
        riesgo = "Bajo: Aprobado"

        # Evaluación de historial crediticio
        if puntuacion < 600:
            riesgo = "Alto: Rechazado"
        elif puntuacion < 750:
            riesgo = "Moderado: Aprobado condicional"

        # Evaluación de ingresos
        if ingresos < 1.5 * cuota:
            riesgo = "Alto: Rechazado"
        elif ingresos < 3 * cuota and riesgo != "Alto: Rechazado":
            riesgo = "Moderado: Aprobado condicional"

        # Evaluación de DTI
        if dti > 50:
            riesgo = "Alto: Rechazado"
        elif dti > 30 and riesgo != "Alto: Rechazado":
            riesgo = "Moderado: Aprobado condicional"

        # Evaluación del empleo
        if tiempo_empleo == 0:
            riesgo = "Alto: Rechazado"
        elif tiempo_empleo < 5 and riesgo != "Alto: Rechazado":
            riesgo = "Moderado: Aprobado condicional"

        # Evaluación de garantías
        if garantia == "Sin garantías":
            riesgo = "Alto: Rechazado"
        elif garantia == "Aval de menor valor" and riesgo != "Alto: Rechazado":
            riesgo = "Moderado: Aprobado condicional"

        # Evaluación de historial de préstamos
        if historial_prestamos == "Deudas en mora":
            riesgo = "Alto: Rechazado"
        elif historial_prestamos == "Retrasos ocasionales" and riesgo != "Alto: Rechazado":
            riesgo = "Moderado: Aprobado condicional"

        messagebox.showinfo("Evaluación de Riesgo", f"Nivel de Riesgo: {riesgo}")
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores válidos.")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Evaluación de Préstamos Bancarios")
root.geometry("400x500")

# Creación de etiquetas y campos de entrada
labels = [
    "Puntuación Crediticia:", "Ingresos Mensuales:", "Cuota del Préstamo:", 
    "Relación Deuda/Ingreso (%):", "Años en el Empleo:"
]
entries = []

for text in labels:
    ttk.Label(root, text=text).pack(pady=5)
    entry = ttk.Entry(root)
    entry.pack()
    entries.append(entry)

entry_puntuacion, entry_ingresos, entry_cuota, entry_dti, entry_tiempo_empleo = entries

# Combo box para Garantías
ttk.Label(root, text="Garantías Presentadas:").pack(pady=5)
combo_garantia = ttk.Combobox(root, values=["Propiedad inmueble", "Aval de alto valor", "Aval de menor valor", "Sin garantías"])
combo_garantia.pack()
combo_garantia.current(0)

# Combo box para Historial de Préstamos
ttk.Label(root, text="Historial de Préstamos Previos:").pack(pady=5)
combo_historial_prestamos = ttk.Combobox(root, values=["Pagados sin retrasos", "Retrasos ocasionales", "Deudas en mora"])
combo_historial_prestamos.pack()
combo_historial_prestamos.current(0)

# Botón para evaluar riesgo
btn_evaluar = ttk.Button(root, text="Evaluar Riesgo", command=evaluar_riesgo)
btn_evaluar.pack(pady=20)

root.mainloop()
