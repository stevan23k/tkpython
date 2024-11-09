import sqlite3
import tkinter as tk
from tkinter import messagebox
 
# Conexión y creación de la base de datos
def conectar_db():
    conexion = sqlite3.connect("personas.db")
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS personas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            edad INTEGER NOT NULL,
            email TEXT NOT NULL
        )
    """)
    conexion.commit()
    conexion.close()
 
# Función para mostrar todos los datos
def mostrar_todos():
    conexion = sqlite3.connect("personas.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM personas")
    registros = cursor.fetchall()
    conexion.close()
 
    tabla_output.delete(1.0, tk.END)
    for registro in registros:
        tabla_output.insert(tk.END, f"ID: {registro[0]}, Nombre: {registro[1]}, Edad: {registro[2]}, Email: {registro[3]}\n")
 
# Función para consultar por ID
def consultar_por_id():
    if id_input.get() == "":
        messagebox.showwarning("Advertencia", "Por favor ingrese un ID para consultar.")
        return
    conexion = sqlite3.connect("personas.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM personas WHERE id = ?", (int(id_input.get()),))
    registro = cursor.fetchone()
    conexion.close()
 
    if registro:
        id_input.delete(0, tk.END)
        id_input.insert(tk.END, str(registro[0]))
        nombre_input.delete(0, tk.END)
        nombre_input.insert(tk.END, registro[1])
        edad_input.delete(0, tk.END)
        edad_input.insert(tk.END, str(registro[2]))
        email_input.delete(0, tk.END)
        email_input.insert(tk.END, registro[3])
        tabla_output.delete(1.0, tk.END)
        tabla_output.insert(tk.END, f"ID: {registro[0]}, Nombre: {registro[1]}, Edad: {registro[2]}, Email: {registro[3]}")
    else:
        messagebox.showinfo("No encontrado", "No se encontró ningún registro con ese ID.")
 
# Función para insertar datos
def insertar():
    if nombre_input.get() == "" or edad_input.get() == "" or email_input.get() == "":
        messagebox.showwarning("Advertencia", "Por favor complete todos los campos.")
        return
   
    nombre = nombre_input.get()
    edad = int(edad_input.get())
    email = email_input.get()
 
    conexion = sqlite3.connect("personas.db")
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO personas (nombre, edad, email)
        VALUES (?, ?, ?)
    """, (nombre, edad, email))
    conexion.commit()
    conexion.close()
 
    messagebox.showinfo("Éxito", f"Persona {nombre} agregada exitosamente.")
    limpiar_campos()
    mostrar_todos()
 
# Función para actualizar datos
def actualizar():
    if id_input.get() == "":
        messagebox.showwarning("Advertencia", "Por favor ingrese un ID para actualizar.")
        return
    id_persona = int(id_input.get())
    nombre = nombre_input.get()
    edad = int(edad_input.get())
    email = email_input.get()
 
    conexion = sqlite3.connect("personas.db")
    cursor = conexion.cursor()
 
    cursor.execute("""
        UPDATE personas
        SET nombre = ?, edad = ?, email = ?
        WHERE id = ?
    """, (nombre, edad, email, id_persona))
    conexion.commit()
    conexion.close()
 
    messagebox.showinfo("Éxito", f"Registro con ID {id_persona} actualizado.")
    limpiar_campos()
    mostrar_todos()
 
# Función para eliminar datos
def eliminar():
    if id_input.get() == "":
        messagebox.showwarning("Advertencia", "Por favor ingrese un ID para eliminar.")
        return
    id_persona = int(id_input.get())
 
    conexion = sqlite3.connect("personas.db")
    cursor = conexion.cursor()
 
    cursor.execute("DELETE FROM personas WHERE id = ?", (id_persona,))
    conexion.commit()
    conexion.close()
 
    messagebox.showinfo("Éxito", f"Registro con ID {id_persona} eliminado.")
    limpiar_campos()
    mostrar_todos()
 
# Función para limpiar campos
def limpiar_campos():
    id_input.delete(0, tk.END)
    nombre_input.delete(0, tk.END)
    edad_input.delete(0, tk.END)
    email_input.delete(0, tk.END)
 
# Crear ventana
ventana = tk.Tk()
ventana.title("Gestión de Personas")
 
# Crear widgets
id_label = tk.Label(ventana, text="ID:")
id_label.grid(row=0, column=0)
id_input = tk.Entry(ventana)
id_input.grid(row=0, column=1)
 
nombre_label = tk.Label(ventana, text="Nombre:")
nombre_label.grid(row=1, column=0)
nombre_input = tk.Entry(ventana)
nombre_input.grid(row=1, column=1)
 
edad_label = tk.Label(ventana, text="Edad:")
edad_label.grid(row=2, column=0)
edad_input = tk.Entry(ventana)
edad_input.grid(row=2, column=1)
 
email_label = tk.Label(ventana, text="Email:")
email_label.grid(row=3, column=0)
email_input = tk.Entry(ventana)
email_input.grid(row=3, column=1)
 
# Botones
insertar_btn = tk.Button(ventana, text="Agregar Persona", command=insertar)
insertar_btn.grid(row=4, column=0)
 
actualizar_btn = tk.Button(ventana, text="Actualizar Persona", command=actualizar)
actualizar_btn.grid(row=4, column=1)
 
eliminar_btn = tk.Button(ventana, text="Eliminar Persona", command=eliminar)
eliminar_btn.grid(row=5, column=0)
 
consultar_btn = tk.Button(ventana, text="Consultar por ID", command=consultar_por_id)
consultar_btn.grid(row=5, column=1)
 
mostrar_todos_btn = tk.Button(ventana, text="Mostrar Todos", command=mostrar_todos)
mostrar_todos_btn.grid(row=6, column=0, columnspan=2)
 
# Área de salida de datos
tabla_output = tk.Text(ventana, height=10, width=50)
tabla_output.grid(row=7, column=0, columnspan=2)
 
# Inicializar base de datos y mostrar registros
conectar_db()
 
ventana.mainloop()