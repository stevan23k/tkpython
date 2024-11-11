import tkinter as tk
import pymysql as mysql
from tkinter import messagebox
import customtkinter


def conexion():
    try:
        conexion = mysql.connect(host="bilu4c9xkyxamq80ka98-mysql.services.clever-cloud.com",
                                port=3306,
                                user="u2lwcsolxlcwbrx2",
                                passwd="YwQK77UnN3nJeDBSaDOY",
                                db="bilu4c9xkyxamq80ka98",
                                cursorclass=mysql.cursors.DictCursor
                                ) 
        print("Conexión exitosa")
        return conexion
    except mysql.MySQLError as e:
        print("Error de conexión:", e)
        return None
# ventana
# Insertar datos en la base de datos
def consultarReservas(correo,):
    connection = conexion()
    if connection:
        try:
            cursor = connection.cursor()  # Return results as dictionary
            cursor.execute("""
                SELECT clientes.nombre, mesas.id_mesa, reservas.fecha, reservas.hora, reservas.nPersonas, clientes.id_cliente, reservas.id_reserva, reservas.estado
                FROM reservas
                LEFT JOIN clientes ON clientes.id_cliente = reservas.id_cliente
                LEFT JOIN mesas ON mesas.id_mesa = reservas.id_mesa
                WHERE clientes.correo = %s;
            """, (correo,))
            
            global resultados
            resultados = cursor.fetchall()
            if resultados:
                global ventana_reserva
                ventana_reserva = customtkinter.CTkToplevel()
                ventana_reserva.title("Lista de Reservas")
                ventana_reserva.geometry("1000x400")

                for i, row in enumerate(resultados):
                    reserva_texto = (f"Cliente: {row['nombre']}, Número de mesa: {row['id_mesa']}, "
                                     f"Fecha: {row['fecha']}, Hora: {row['hora']}, "
                                     f"Número de personas: {row['nPersonas']}, Estado: {row['estado']}")
                    label_reserva = customtkinter.CTkLabel(ventana_reserva, text=reserva_texto)
                    label_reserva.grid(row=i, column=0, padx=10, pady=5, sticky="w")
                    
                    # cancelar reserva
                    def cancelarReserva(id_reserva, ventana, nombre, mesa):
                        connection = conexion()
                        if connection:
                            try:
                                cursor = connection.cursor()
                                cursor.execute("update reservas set estado = false where id_reserva = %s", (id_reserva,))
                                cursor.execute("update mesas set ocupado = false where id_mesa = %s", (mesa,))
                                connection.commit()
                                print(f"Reserva con ID {id_reserva} su reserva ha sido cancelada.")
                                messagebox.showinfo("cancelada", f"Reserva cancelada correctamente señor {nombre}")
                                ventana.destroy()
                                consultarReservas(correo)
                            except mysql.MySQLError as e:
                                print("Error al eliminar reserva:", e)
                            finally:
                                connection.close()
                    
                    btn_cancelar = customtkinter.CTkButton(
                        ventana_reserva, text="Cancelar reserva",
                        fg_color="red",
                        hover_color="red",
                        command=lambda r=row: cancelarReserva(r['id_reserva'], ventana_reserva,{row['nombre']}, {row['id_mesa']})
                    )
                    btn_cancelar.grid(row=i, column=2, padx=10, pady=5)
            else:
                print("No se encontraron registros.")
                
        except mysql.MySQLError as e:
            print("Error al consultar datos:", e)
        finally:
            connection.close()
# Consultar datos desde la base de datos
def consultar_datos():
    connection = conexion()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM clientes")
            resultados = cursor.fetchall()
            if resultados:
                # Crear una nueva ventana para mostrar los clientes
                global ventana_clientes
                ventana_clientes = customtkinter.CTkToplevel()
                ventana_clientes.title("Lista de Clientes")
                ventana_clientes.geometry("1000x400")

                # Crear etiquetas y botones para cada cliente
                for i, row in enumerate(resultados):
                    cliente_texto = f"id_cliente: {row['id_cliente']}, nombre: {row['nombre']}, correo: {row['correo']}, telefono: {row['telefono']}"
                    label_cliente = customtkinter.CTkLabel(ventana_clientes, text=cliente_texto)
                    label_cliente.grid(row=i, column=0, padx=10, pady=5, sticky="w")
                    
                    # Botón de Editar
                    btn_editar = customtkinter.CTkButton(ventana_clientes, text="Editar", command=lambda r=row: editar_cliente(r['id_cliente']))
                    btn_editar.grid(row=i, column=1, padx=10, pady=5)

                    # Botón de Eliminar
                    btn_eliminar = customtkinter.CTkButton(ventana_clientes, text="Eliminar", command=lambda r=row: eliminar_cliente(r['id_cliente'], ventana_clientes))
                    btn_eliminar.grid(row=i, column=2, padx=10, pady=5)
                    
            else:
                print("No se encontraron registros.")
        except mysql.MySQLError as e:
            print("Error al consultar datos:", e)
        finally:
            connection.close()

# Función para editar un cliente
def editar_cliente(id_cliente):
    def guardar_cliente(id_cliente, nombre, correo, telefono, ventana):
        connection = conexion()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("UPDATE clientes SET nombre = %s, correo = %s, telefono = %s WHERE id_cliente = %s", (nombre, correo, telefono, id_cliente))
                connection.commit()
                print(f"Cliente con ID {id_cliente} actualizado.")
                ventana.destroy()
                consultar_datos()

                messagebox.showinfo("Guardado", "Cliente actualizado correctamente")
                ventana_editar.destroy()
                ventana_clientes.destroy()
            except mysql.MySQLError as e:
                print("Error al editar cliente:", e)
            finally:
                connection.close()

    print(f"Editar cliente con ID: {id_cliente}") 
    connection = conexion()
    if connection:
        try:
            ventana_editar = customtkinter.CTkToplevel()
            ventana_editar.title("Editar Cliente")
            ventana_editar.geometry("1000x400")
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM clientes WHERE id_cliente = %s", (id_cliente,))
            cliente = cursor.fetchone()
            if cliente:
                label_nombre = customtkinter.CTkLabel(ventana_editar, text="Nombre:")
                label_nombre.pack(pady=5)
                entry_nombre = customtkinter.CTkEntry(ventana_editar)
                entry_nombre.insert(0, cliente['nombre'])
                entry_nombre.pack(pady=5)

                label_correo = customtkinter.CTkLabel(ventana_editar, text="Correo:")
                label_correo.pack(pady=5)
                entry_correo = customtkinter.CTkEntry(ventana_editar)
                entry_correo.insert(0, cliente['correo'])
                entry_correo.pack(pady=5)
                
                label_telefono = customtkinter.CTkLabel(ventana_editar, text="Telefono:")
                label_telefono.pack(pady=5)
                entry_telefono = customtkinter.CTkEntry(ventana_editar)
                entry_telefono.insert(0, cliente['telefono'])
                entry_telefono.pack(pady=5)

                # Botón de Guardar
                boton_editar = customtkinter.CTkButton(ventana_editar, text="Guardar", command=lambda: guardar_cliente(id_cliente, entry_nombre.get(), entry_correo.get(), entry_telefono.get(), ventana_editar))
                boton_editar.pack(pady=10)
                # Botón de Cancelar
                boton_cancelar = customtkinter.CTkButton(ventana_editar, text="Cancelar", command=ventana_editar.destroy)
                boton_cancelar.pack(padx=10)
        except mysql.MySQLError as e:
            print("Error al editar cliente:", e)                
    
# Función para eliminar un cliente
def eliminar_cliente(id_cliente, ventana):
    connection = conexion()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (id_cliente,))
            connection.commit()
            print(f"Cliente con ID {id_cliente} eliminado.")
            # Cierra y vuelve a abrir la ventana para refrescar la lista
            ventana.destroy()
            consultar_datos()
        except mysql.MySQLError as e:
            print("Error al eliminar cliente:", e)
        finally:
            connection.close()
          
# Configurar la interfaz de usuario
app = customtkinter.CTk()
app.geometry("1000x500")
app.title("Consultar reserva")

# Crear y posicionar los elementos de la interfaz
label_correo = customtkinter.CTkLabel(app, text="Correo:")
label_correo.pack(pady=5)
entry_correo = customtkinter.CTkEntry(app)
entry_correo.pack(pady=5)

boton_consultar = customtkinter.CTkButton(app, text="Consultar", command=lambda: consultarReservas(entry_correo.get()))
boton_consultar.pack(pady=10)


boton_editar = customtkinter.CTkButton(app, text="Editar", command=consultar_datos)
boton_editar.pack(pady=10)

"""
label_nombre = customtkinter.CTkLabel(admin, text="Nombre:")
label_nombre.pack(pady=5)

entry_nombre = customtkinter.CTkEntry(admin)
entry_nombre.pack(pady=5)

label_telefono = customtkinter.CTkLabel(admin, text="Telefono:")
label_telefono.pack(pady=5)

entry_telefono = customtkinter.CTkEntry(admin)
entry_telefono.pack(pady=5)

boton_insertar = customtkinter.CTkButton(admin, text="Insertar", command=insertar_datos)
boton_insertar.pack(pady=10)

btn_mostrar_clientes = customtkinter.CTkButton(admin, text="Mostrar Clientes", command=consultar_datos)
btn_mostrar_clientes.pack(pady=5)
"""

app.mainloop()

