import os
import tkinter as tk
from tkinter import ttk, messagebox
from database import inicializar_bd, agregar_transaccion, obtener_transacciones_del_dia, obtener_datos_producto
from pdf_generator import generar_reporte
from datetime import datetime

def agregar_venta_gui():
    fecha = datetime.now().strftime('%Y-%m-%d')
    tipo = "Ingreso"
    identificador = entry_descripcion.get()  # Puede ser índice o nombre del producto
    cantidad = float(entry_cantidad.get())

    # Obtener datos del producto desde el archivo Excel
    nombre_producto, precio_venta, precio_original = obtener_datos_producto(identificador)

    if precio_venta is None or precio_original is None:
        messagebox.showerror("Error", f"El producto con identificador '{identificador}' no se encuentra en el archivo Excel.")
        return

    ganancia = (precio_venta - precio_original) * cantidad
    monto_total = cantidad * precio_venta

    agregar_transaccion(fecha, tipo, cantidad, nombre_producto, precio_venta, precio_original, ganancia, monto_total)
    
    # Agregar datos a la tabla
    tree.insert('', 'end', values=(nombre_producto, cantidad, precio_venta, monto_total, ganancia))
    
    messagebox.showinfo("Éxito", "Venta agregada correctamente.")
    entry_cantidad.delete(0, tk.END)
    entry_descripcion.delete(0, tk.END)


def generar_reporte_gui(root):  # Ahora 'root' es un argumento de la función
    transacciones_hoy = obtener_transacciones_del_dia()
    if not transacciones_hoy:
        messagebox.showinfo("Sin datos", "No hay transacciones para el día actual.")
        return
    
    # Generar el reporte
    generar_reporte(transacciones_hoy)

    # Mostrar cuadro de éxito
    messagebox.showinfo("Éxito", "Reporte generado con éxito para el día actual.")

    # Preguntar si desea ver el PDF
    respuesta = messagebox.askyesno("Ver PDF", "¿Deseas ver el reporte en PDF?")

    if respuesta:  # Si el usuario selecciona 'Sí'
        # Obtener la ruta del archivo generado
        fecha_actual = datetime.now().strftime('%Y-%m-%d')
        ruta_pdf = r"c:\Users\KJhonatan\OneDrive\Escritorio\mi_taller\reporte_" + fecha_actual + ".pdf"
        
        # Intentar abrir el PDF con el visor predeterminado
        try:
            os.startfile(ruta_pdf)  # Abrir el PDF con la aplicación predeterminada
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo PDF: {e}")

        # Cerrar la aplicación
        root.quit()  # Ahora 'root' se pasa como argumento y se puede usar para cerrar la aplicación


def iniciar_interfaz():
    inicializar_bd()
    global entry_cantidad, entry_descripcion, tree

    root = tk.Tk()
    root.title("Control de Ventas - Taller")

    # Entradas de datos
    tk.Label(root, text="Índice o Nombre del producto:").grid(row=0, column=0)
    entry_descripcion = tk.Entry(root)
    entry_descripcion.grid(row=0, column=1)

    tk.Label(root, text="Cantidad:").grid(row=1, column=0)
    entry_cantidad = tk.Entry(root)
    entry_cantidad.grid(row=1, column=1)

    tk.Button(root, text="Agregar Venta", command=agregar_venta_gui).grid(row=2, column=0, columnspan=2)
    tk.Button(root, text="Generar Reporte", command=lambda: generar_reporte_gui(root)).grid(row=3, column=0, columnspan=2)

    # Tabla para mostrar datos
    tree = ttk.Treeview(root, columns=("Nombre", "Cantidad", "Precio de Venta", "Monto Total", "Ganancia"), show="headings")
    tree.grid(row=4, column=0, columnspan=2)

    # Configuración de encabezados de la tabla
    tree.heading("Nombre", text="Nombre")
    tree.heading("Cantidad", text="Cantidad")
    tree.heading("Precio de Venta", text="Precio de Venta")
    tree.heading("Monto Total", text="Monto Total")
    tree.heading("Ganancia", text="Ganancia")
    
    root.mainloop()  # Iniciar la interfaz gráfica de la aplicación
