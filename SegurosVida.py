import tkinter as tk
from tkinter import messagebox, ttk
import rule_engine
import concurrent.futures

# Reglas de evaluación de riesgo
reglas_riesgo = {
    "bajo": rule_engine.Rule(
        "(edad < 30) and "
        "(salud == 'saludable') and "
        "(historial_familiar == 'false') and "
        "(estilo_vida == 'activo') and "
        "(ocupacion == 'oficina') and "
        "(historial_seguro == 'bueno')"
    ),
    "alto": rule_engine.Rule(
        "(edad > 50) or ((salud in ['diabetes', 'hipertension', 'obesidad']) or "
        "(historial_familiar == 'true') or "
        "(estilo_vida in ['fumador', 'alcoholico']) or "
        "(ocupacion in ['piloto', 'bombero']))"
    ),
    "moderado": rule_engine.Rule(
        "(edad >= 30 and edad <= 50) or "
        "(salud in ['diabetes', 'hipertension', 'obesidad']) or "
        "(historial_familiar == 'true') or "
        "(estilo_vida in ['fumador', 'alcoholico']) or"
        "(edad > 50 ) or "
        "(historial_seguro == 'malo')"
    )
}

def evaluar_riesgo(cliente):
    """Evalúa el nivel de riesgo basado en las reglas definidas."""
    if reglas_riesgo["bajo"].matches(cliente):
        return "Bajo Riesgo"
    elif reglas_riesgo["alto"].matches(cliente):
        return "Alto Riesgo"
    elif reglas_riesgo["moderado"].matches(cliente):
        return "Moderado Riesgo"
    return "Desconocido"

def obtener_datos():
    """Obtiene los datos de la interfaz y evalúa el riesgo."""
    try:
        cliente = {
            "nombre": entry_nombre.get(),
            "edad": int(entry_edad.get()),  # Validación numérica
            "salud": combo_salud.get(),
            "historial_familiar": combo_historial_familiar.get(),
            "estilo_vida": combo_estilo_vida.get(),
            "ocupacion": combo_ocupacion.get(),
            "historial_seguro": combo_historial_seguro.get(),
        }

        # Evaluación en paralelo
        with concurrent.futures.ThreadPoolExecutor() as executor:
            resultado_futuro = executor.submit(evaluar_riesgo, cliente)
            nivel_riesgo = resultado_futuro.result()

        messagebox.showinfo("Resultado", f"Cliente: {cliente['nombre']}\nNivel de Riesgo: {nivel_riesgo}")

    except ValueError:
        messagebox.showerror("Error", "La edad debe ser un número válido.")

# Crear ventana
root = tk.Tk()
root.title("Cuestionario de Evaluación de Riesgo")
root.geometry("400x400")

# Etiquetas y entradas
tk.Label(root, text="Nombre:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_nombre = tk.Entry(root)
entry_nombre.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Edad:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_edad = tk.Entry(root)
entry_edad.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Salud:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
combo_salud = ttk.Combobox(root, values=["saludable", "diabetes", "hipertension", "obesidad"])
combo_salud.grid(row=2, column=1, padx=10, pady=5)
combo_salud.current(0)

tk.Label(root, text="Historial Familiar:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
combo_historial_familiar = ttk.Combobox(root, values=["true", "false"])
combo_historial_familiar.grid(row=3, column=1, padx=10, pady=5)
combo_historial_familiar.current(1)

tk.Label(root, text="Estilo de Vida:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
combo_estilo_vida = ttk.Combobox(root, values=["activo", "fumador", "alcoholico"])
combo_estilo_vida.grid(row=4, column=1, padx=10, pady=5)
combo_estilo_vida.current(0)

tk.Label(root, text="Ocupación:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
combo_ocupacion = ttk.Combobox(root, values=["oficina", "piloto", "bombero"])
combo_ocupacion.grid(row=5, column=1, padx=10, pady=5)
combo_ocupacion.current(0)

tk.Label(root, text="Historial de Seguro:").grid(row=6, column=0, padx=10, pady=5, sticky="w")
combo_historial_seguro = ttk.Combobox(root, values=["bueno", "malo"])
combo_historial_seguro.grid(row=6, column=1, padx=10, pady=5)
combo_historial_seguro.current(0)

# Botón para evaluar
btn_enviar = tk.Button(root, text="Evaluar Riesgo", command=obtener_datos)
btn_enviar.grid(row=7, column=0, columnspan=2, pady=20)

# Ejecutar aplicación
root.mainloop()

