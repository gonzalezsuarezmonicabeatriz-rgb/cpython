import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from statistics import mean

class CompuestoQuimico:

    def __init__(self, nombre, formula, peso):
        self.__nombre = nombre
        self.__formula = formula
        self.__peso = peso

    def get_nombre(self):
        return self.__nombre

    def mostrar_info(self):

        return f"""
Nombre: {self.__nombre}
Fórmula: {self.__formula}
Peso molecular: {self.__peso}
"""

class EnsayoExperimental:

    def __init__(self, compuesto, protocolo):

        self.compuesto = compuesto
        self.protocolo = protocolo

        self.concentraciones = []
        self.lecturas = []

    def agregar_dato(self, concentracion, lectura):

        self.concentraciones.append(concentracion)
        self.lecturas.append(lectura)

    def calcular_promedio(self):

        if len(self.lecturas) == 0:
            return 0

        return round(mean(self.lecturas), 3)

    def calcular_ic50(self):

        promedio = self.calcular_promedio()

        if promedio > 0.8:
            return "IC50 ALTA"
        elif promedio > 0.5:
            return "IC50 MEDIA"
        else:
            return "IC50 BAJA"

    def generar_reporte(self):

        reporte = f"""

{self.compuesto.mostrar_info()}

Equipo: {self.protocolo["equipo"]}
Modo: {self.protocolo["modo"]}
Longitud de onda: {self.protocolo["longitud_onda"]} nm

{self.concentraciones}

Lecturas:
{self.lecturas}

{self.calcular_promedio()}

Predicción biológica:
{self.calcular_ic50()}
"""

        return reporte


protocolos = {

    "BioTek": {
        "equipo": "BioTek",
        "modo": "Absorbancia",
        "longitud_onda": 570
    },

    "ThermoFisher": {
        "equipo": "ThermoFisher",
        "modo": "Fluorescencia",
        "longitud_onda": 485
    },

    "Agilent": {
        "equipo": "Agilent",
        "modo": "Luminescencia",
        "longitud_onda": 530
    }
}


def agregar_dato():

    try:

        concentracion = float(entry_concentracion.get())
        lectura = float(entry_lectura.get())

        lista_concentraciones.insert(
            tk.END,
            f"{concentracion}"
        )

        lista_lecturas.insert(
            tk.END,
            f"{lectura}"
        )

        entry_concentracion.delete(0, tk.END)
        entry_lectura.delete(0, tk.END)

    except:
        resultado.delete("1.0", tk.END)
        resultado.insert(
            tk.END,
            "ERROR: Ingresa valores numéricos válidos."
        )


def ejecutar_analisis():

    try:

        nombre = entry_nombre.get()
        formula = entry_formula.get()
        peso = float(entry_peso.get())

        compuesto = CompuestoQuimico(
            nombre,
            formula,
            peso
        )

        protocolo_seleccionado = combo_protocolos.get()

        ensayo = EnsayoExperimental(
            compuesto,
            protocolos[protocolo_seleccionado]
        )

        concentraciones = lista_concentraciones.get(0, tk.END)
        lecturas = lista_lecturas.get(0, tk.END)

        for c, l in zip(concentraciones, lecturas):

            ensayo.agregar_dato(
                float(c),
                float(l)
            )

        reporte = ensayo.generar_reporte()

        resultado.delete("1.0", tk.END)
        resultado.insert(tk.END, reporte)

    except:

        resultado.delete("1.0", tk.END)

        resultado.insert(
            tk.END,
            "ERROR: Verifica todos los datos."
        )


ventana = tk.Tk()

ventana.title(
    "Plataforma de Cribado Farmacológico"
)

ventana.geometry("900x700")


titulo = tk.Label(
    ventana,
    text="Sistema de Análisis de Citotoxicidad",
    font=("Arial", 18, "bold")
)

titulo.pack(pady=10)


frame_datos = tk.Frame(ventana)

frame_datos.pack(pady=10)

tk.Label(
    frame_datos,
    text="Nombre del compuesto:"
).grid(row=0, column=0)

entry_nombre = tk.Entry(frame_datos, width=30)

entry_nombre.grid(row=0, column=1)

tk.Label(
    frame_datos,
    text="Fórmula molecular:"
).grid(row=1, column=0)

entry_formula = tk.Entry(frame_datos, width=30)

entry_formula.grid(row=1, column=1)

tk.Label(
    frame_datos,
    text="Peso molecular:"
).grid(row=2, column=0)

entry_peso = tk.Entry(frame_datos, width=30)

entry_peso.grid(row=2, column=1)

tk.Label(
    frame_datos,
    text="Protocolo:"
).grid(row=3, column=0)

combo_protocolos = ttk.Combobox(
    frame_datos,
    values=list(protocolos.keys()),
    width=27
)

combo_protocolos.grid(row=3, column=1)

combo_protocolos.current(0)


frame_exp = tk.Frame(ventana)

frame_exp.pack(pady=10)


tk.Label(
    frame_exp,
    text="Concentración:"
).grid(row=0, column=0)

entry_concentracion = tk.Entry(frame_exp)

entry_concentracion.grid(row=0, column=1)


tk.Label(
    frame_exp,
    text="Lectura:"
).grid(row=1, column=0)

entry_lectura = tk.Entry(frame_exp)

entry_lectura.grid(row=1, column=1)

boton_agregar = tk.Button(
    frame_exp,
    text="Agregar dato",
    command=agregar_dato,
    bg="lightblue"
)

boton_agregar.grid(row=2, column=0, columnspan=2, pady=10)


frame_listas = tk.Frame(ventana)

frame_listas.pack(pady=10)


tk.Label(
    frame_listas,
    text="Concentraciones"
).grid(row=0, column=0)

lista_concentraciones = tk.Listbox(
    frame_listas,
    width=20,
    height=8
)

lista_concentraciones.grid(row=1, column=0)

tk.Label(
    frame_listas,
    text="Lecturas"
).grid(row=0, column=1)

lista_lecturas = tk.Listbox(
    frame_listas,
    width=20,
    height=8
)

lista_lecturas.grid(row=1, column=1)

boton_analizar = tk.Button(
    ventana,
    text="Ejecutar análisis",
    command=ejecutar_analisis,
    bg="lightgreen",
    font=("Arial", 12, "bold")
)

boton_analizar.pack(pady=15)


resultado = ScrolledText(
    ventana,
    width=100,
    height=20
)

resultado.pack(pady=10)

ventana.mainloop()
