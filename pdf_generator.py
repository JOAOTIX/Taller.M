import os
from fpdf import FPDF
from datetime import datetime

class PDF(FPDF):
    def __init__(self, transacciones):
        super().__init__()
        self.transacciones = transacciones  # Almacenar las transacciones como un atributo

    def header(self):
        # Título del reporte con la fecha
        fecha_actual = datetime.now().strftime('%d-%m-%Y')
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, f'Ventas del día: {fecha_actual}', 0, 1, 'C')
        self.ln(10)

        # Mostrar el mensaje personalizado con las ganancias y lo que se debe dejar en la lata
        total_ganancia = 0
        total_monto = 0
        for t in self.transacciones:
            ganancia = t[7]
            monto_total = t[8]
            total_ganancia += ganancia
            total_monto += monto_total

        monto_a_dejar = total_monto - total_ganancia

        self.set_font('Arial', '', 12)
        self.cell(0, 10, f"Hola mami, tu ganancia el día de hoy es: {total_ganancia:.2f}", 0, 1, 'C')
        self.cell(0, 10, f"El monto que debes dejar en la lata es: {monto_a_dejar:.2f}", 0, 1, 'C')
        self.cell(0, 10, f"Te amo mami y no olvides respetar estos informes para que puedas cuidar tu ahorro:3", 0, 1, 'C')
        self.ln(10)

    def agregar_tabla(self):
        self.set_font('Arial', 'B', 10)
        self.cell(80, 10, "Nombre", 1, 0, 'C')
        self.cell(20, 10, "Cantidad", 1, 0, 'C')
        self.cell(30, 10, "Precio Venta", 1, 0, 'C')
        self.cell(30, 10, "Monto Total", 1, 0, 'C')
        self.cell(20, 10, "Ganancia", 1, 1, 'C')

        self.set_font('Arial', '', 10)
        total_ganancia = 0
        total_monto = 0

        for t in self.transacciones:
            nombre = t[4]
            cantidad = t[3]
            precio_venta = t[5]
            monto_total = t[8]
            ganancia = t[7]

            self.cell(80, 10, nombre, 1, 0, 'C')
            self.cell(20, 10, f"{cantidad:.2f}", 1, 0, 'C')
            self.cell(30, 10, f"{precio_venta:.2f}", 1, 0, 'C')
            self.cell(30, 10, f"{monto_total:.2f}", 1, 0, 'C')
            self.cell(20, 10, f"{ganancia:.2f}", 1, 1, 'C')

            total_ganancia += ganancia
            total_monto += monto_total

        # Agregar totales al final
        self.set_font('Arial', 'B', 10)
        self.cell(130, 10, "Totales:", 1, 0, 'C')
        self.cell(30, 10, f"{total_monto:.2f}", 1, 0, 'C')
        self.cell(20, 10, f"{total_ganancia:.2f}", 1, 1, 'C')


def generar_reporte(transacciones):
    fecha_actual = datetime.now().strftime('%Y-%m-%d')
    ruta = r"c:\Users\KJhonatan\OneDrive\Escritorio\mi_taller\reporte_" + fecha_actual + ".pdf"

    # Crear la instancia del PDF y pasar las transacciones
    pdf = PDF(transacciones)  # Pasar las transacciones aquí
    
    pdf.add_page()
    pdf.agregar_tabla()

    try:
        pdf.output(ruta)
        print(f"Reporte generado exitosamente: {ruta}")
    except PermissionError:
        print(f"No se puede generar el archivo '{ruta}'. Asegúrate de que no esté abierto en otro programa.")
